#include <avr/io.h>
#include <avr/interrupt.h>
#define F_CPU 16E6 // used in _delay_ms, 16 MHz
#include <util/delay.h>
#include <stdio.h>
#include <stdlib.h>

// Definitions
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#define bit_is_set(sfr, bit) (_SFR_BYTE(sfr) & _BV(bit))
#define BAUDRATE 9600
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)
#define HIGH 0x1
#define LOW  0x0
#define OUTPUT 0x1
#define INPUT  0x0

// Functions
void USART_init(void);
unsigned char USART_receive(void);
void USART_send( unsigned char data);
void USART_putstring(char* StringPtr);
void toggleMode(void);
void sendMode(void);
void sendState(void);
void readTempSensor(void);
void writeTempSensor(void);
void readLightSensor(void);
void writeLightSensor(void);
void setPinMode(char type, int pin, uint8_t val);
void setPinValue(char type, int pin, uint8_t val);
void executeTasks(void);
void handleCommands(void);
void rollIn(void);
void rollOut(void);
void turnOffYellow(void);
void handleRolling(void);
int analogRead(uint8_t pin);

// Setting up pin layout
int redPin = 8; // Digital
int greenPin = 10; // Digital
int yellowPin = 9; // Digital
int lightSensorPin = 0; // Analog
int tempSensorPin = 1; // Analog

// Default values
uint16_t analogValue = 0;
uint16_t analogTemp = 0;
uint16_t analogLight = 0;
float floorTemp = 0.0;
float ceilTemp = 15.0;
float ceilLight = 800.0;

// Read values
float temperature = 0.0;
float lightIntensity = 0.0;

// Timers
uint32_t TTR_read_temp_sensor = 0;
uint32_t TTR_read_light_sensor = 0;
uint32_t TTR_transmit_readings = 0;
uint32_t TTR_turn_off_yellow = 0;
uint32_t TTR_handle_rolling = 0;

uint32_t timer_read_temp_sensor = 5;
uint32_t timer_read_light_sensor = 5;
uint32_t timer_transmit_readings = 5;
uint32_t timer_turn_off_yellow = 5;
uint32_t timer_handle_rolling = 5;

uint32_t timer_enable_read_temp_sensor = 1;
uint32_t timer_enable_read_light_sensor = 1;
uint32_t timer_enable_transmit_readings = 1;
uint32_t timer_enable_turn_off_yellow = 0;
uint32_t timer_enable_handle_rolling = 1;

// Translation table
typedef enum {
	SEND_TEMP		= 0,
	SEND_LIGHT		= 1,
	CHANGE_MODE		= 2,
	SEND_MODE		= 3,
	SEND_STATE		= 4,
	ROLL_OUT		= 5,
	ROLL_IN			= 6,
	INC_TEMP		= 7,
	DEC_TEMP		= 8,
	INC_LIGHT		= 9,
	DEC_LIGHT		= 10
} COMMANDS;

// Screen rolling
typedef enum {ROLLED_IN=0, ROLLED_OUT=1, ROLLING=2} STATES;
STATES state = ROLLED_IN;
typedef enum{AUTO=0, MANUAL=1} MODES;
MODES mode = AUTO;
uint8_t changeCount = 0;
uint8_t countTillChange = 2;
STATES nextState;

int main() {
	// LEDs (D)igital
	setPinMode('D', greenPin, OUTPUT);
	setPinMode('D', yellowPin, OUTPUT);
	setPinMode('D', redPin, OUTPUT);

	// Sensor pins (A)nalog
	setPinMode('A', lightSensorPin, INPUT);
	setPinMode('A', tempSensorPin, INPUT);

	// Set up serial
	USART_init();

	// Enable ADC
	ADMUX |= (1<<REFS0);
	ADCSRA |= (1<<ADEN) | (1<<ADPS0) | (1<<ADPS1) | (1<<ADPS2);

	// Initialize timer
	TCCR1B = (1 << CS12) | (1 << WGM12); // prescaler set to 256 (CTC mode)
	TIMSK1 = 1 << OCIE1A; // Timer 1 Output Compare A Match Interrupt Enable
	OCR1A = (uint16_t)625; // 10ms = (256/16.000.000)*625
	sei();
	nextState = state;

	// Default to rolled in
	setPinValue('D', yellowPin, LOW);
	setPinValue('D', redPin, HIGH);
	setPinValue('D', greenPin, LOW);

	while(1) {
		handleCommands();
	}
}

// Ticks every 10ms
ISR (TIMER1_COMPA_vect) {
	// Decrement all TimeToRuns

	if(timer_enable_read_temp_sensor && TTR_read_temp_sensor > 0)
	TTR_read_temp_sensor--;
	if(timer_enable_read_light_sensor && TTR_read_light_sensor > 0)
	TTR_read_light_sensor--;
	if(timer_enable_transmit_readings && TTR_transmit_readings > 0)
	TTR_transmit_readings--;
	if(timer_enable_handle_rolling && TTR_handle_rolling > 0)
	TTR_handle_rolling--;
	if(timer_enable_turn_off_yellow && TTR_turn_off_yellow > 0)
	TTR_turn_off_yellow--;

	executeTasks();

}

void toggleMode(void) {
	if(mode == MANUAL)
	mode = AUTO;
	else
	mode = MANUAL;

	// Transmit
	sendMode();
}

void executeTasks(void) {
	if(timer_enable_read_temp_sensor && TTR_read_temp_sensor == 0) {
		readTempSensor();
		TTR_read_temp_sensor = timer_read_temp_sensor * 100; // Turn seconds into n*10ms
	}
	if(timer_enable_read_light_sensor && TTR_read_light_sensor == 0) {
		readLightSensor();
		TTR_read_light_sensor = timer_read_light_sensor * 100; // Turn seconds into n*10ms
	}
	if(timer_enable_transmit_readings && TTR_transmit_readings == 0) {
		writeTempSensor();
		writeLightSensor();
		TTR_transmit_readings = timer_transmit_readings * 100; // Turn seconds into n*10ms
	}
	if(timer_enable_handle_rolling && TTR_handle_rolling == 0) {
		handleRolling();
		TTR_handle_rolling = timer_handle_rolling * 100;
	}
	if(timer_enable_turn_off_yellow && TTR_turn_off_yellow == 0) {
		turnOffYellow();
		timer_enable_turn_off_yellow = 0; // Turn it off
		TTR_turn_off_yellow = timer_turn_off_yellow * 100;
	}
}

void sendMode(void) {
	USART_send(SEND_MODE);
	char str[12];
	sprintf(str, "%d", mode);
	USART_putstring(str);
}

void sendState(void) {
	USART_send(SEND_STATE);
	char str[12];
	sprintf(str, "%d", state);
	USART_putstring(str);
}

void handleCommands(void) {
	unsigned char a = USART_receive();

	switch(a) {
		case ROLL_IN:
		mode = MANUAL;
		sendMode();
		rollIn();
		break;

		case ROLL_OUT:
		mode = MANUAL;
		sendMode();
		rollOut();
		break;

		case CHANGE_MODE:
		toggleMode();
		break;

		case INC_TEMP:
		if(ceilTemp < 1000){
			ceilTemp  += 2; // Increase by 2

			// Send it to the PC aswell for syncing
			USART_send(INC_TEMP);
		}

		break;

		case DEC_TEMP:
		if(ceilTemp > 2) {
			ceilTemp -= 2; // Decrease by 2

			// Send it to the PC aswell for syncing
			USART_send(DEC_TEMP);
		}
		break;

		case INC_LIGHT:
		if(ceilLight < 1020) {
			ceilLight += 25; // Increase by 25

			// Send it to the PC aswell for syncing
			USART_send(INC_LIGHT);
		}
		break;

		case DEC_LIGHT:
		if(ceilLight > 25) {
			ceilLight -= 25; // Decrease by 25

			// Send it to the PC aswell for syncing
			USART_send(DEC_LIGHT);
		}
		break;

		// Ignore Arduino > PC commands
		case SEND_TEMP:
		case SEND_LIGHT:
		case SEND_MODE:
		case SEND_STATE:
		break;
	}
}

void rollIn(void) {
	nextState = ROLLED_IN;
	state = ROLLING;
	sendState();

	setPinValue('D', yellowPin, HIGH);
	setPinValue('D', redPin, HIGH);
	setPinValue('D', greenPin, LOW);

	timer_enable_turn_off_yellow = 1;
	TTR_turn_off_yellow = timer_turn_off_yellow * 100; // Turn seconds into n*10ms
}

void rollOut(void) {
	nextState = ROLLED_OUT;
	state = ROLLING;
	sendState();

	setPinValue('D', yellowPin, HIGH);
	setPinValue('D', greenPin, HIGH);
	setPinValue('D', redPin, LOW);

	timer_enable_turn_off_yellow = 1;
	TTR_turn_off_yellow = timer_turn_off_yellow * 100; // Turn seconds into n*10ms
}

void turnOffYellow(void) {
	state = nextState;
	sendState();
	setPinValue('D', yellowPin, LOW);
}

void handleRolling(void) {
	if(mode == MANUAL)
	return;
	if(state == ROLLING)
	return;

	STATES tState;
	tState = state;

	if( analogLight >= ceilLight && !(temperature <= ceilTemp)) {
		tState = ROLLED_OUT;
	}
	if( analogLight < ceilLight || temperature <= ceilTemp ) {
		tState = ROLLED_IN;
	}

	if(tState != state)
	changeCount++;
	else
	changeCount = 0;

	if(changeCount >= countTillChange) {
		switch(tState) {
			case ROLLED_IN:
			rollIn();
			break;
			case ROLLED_OUT:
			rollOut();
			break;
			case ROLLING:
			break;
		}
		changeCount = 0;
	}
}

void readTempSensor(void) {
	analogRead(tempSensorPin);  // switch the channel to A0 and hold for 104µs
	analogTemp = analogRead(tempSensorPin); // proper readout

	// Calculate temperature
	float voltage = analogTemp * 5.0 / 1024;
	temperature = (voltage - 0.5) * 100;
}

void writeTempSensor(void) {
	USART_send(SEND_TEMP);

	char str[12];
	sprintf(str, "%d", analogTemp);
	USART_putstring(str);
}

void readLightSensor(void) {
	analogRead(lightSensorPin);  // switch the channel to A0 and hold for 104µs
	analogLight = analogRead(lightSensorPin); // proper readout

	lightIntensity = analogLight + 0.0;
}

void writeLightSensor(void) {
	USART_send(SEND_LIGHT);

	char str[12];
	sprintf(str, "%d", analogLight);
	USART_putstring(str);
}

/*
PORTD maps to Arduino digital pins 0 to 7
PORTB maps to Arduino digital pins 8 to 13 The two high bits (6 & 7) map to the crystal pins and are not usable
PORTC maps to Arduino analog pins 0 to 5. Pins 6 & 7 are only accessible on the Arduino Mini

DDRC - The Port C Data Direction Register - read/write
PORTC - The Port C Data Register - read/write
PINC - The Port C Input Pins Register - read only
*/
// Pin stuff
void setPinMode(char type, int pin, uint8_t val) {
	switch(type) {
		case 'D':
		if(pin >= 8) {
			pin -= 8;
			if (val == LOW) {
				DDRB &= ~(_BV(pin)); // clear bit
				} else {
				DDRB |= _BV(pin); // set bit
			}
			} else {
			if (val == LOW) {
				DDRD &= ~(_BV(pin)); // clear bit
				} else {
				DDRD |= _BV(pin); // set bit
			}
		}

		break;

		case 'A':
		case 'C':
		if (val == LOW) {
			DDRC &= ~(_BV(pin)); // clear bit
			} else {
			DDRC |= _BV(pin); // set bit
		}
		break;
	}
}

void setPinValue(char type, int pin, uint8_t val) {
	switch(type) {
		case 'D':
		if(pin >= 8) {
			pin -= 8;
			if (val == LOW) {
				PORTB &= ~(_BV(pin)); // clear bit
				} else {
				PORTB |= _BV(pin); // set bit
			}
			} else {
			if (val == LOW) {
				PORTD &= ~(_BV(pin)); // clear bit
				} else {
				PORTD |= _BV(pin); // set bit
			}
		}

		break;

		case 'A':
		case 'C':
		if (val == LOW) {
			PORTC &= ~(_BV(pin)); // clear bit
			} else {
			PORTC |= _BV(pin); // set bit
		}
		break;
	}
}

void USART_init(void) {
	UBRR0H = (uint8_t)((int)BAUD_PRESCALLER>>8);
	UBRR0L = (uint8_t)((int)BAUD_PRESCALLER);
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00); /* 8-bit data */
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);   /* Enable RX and TX */
}

unsigned char USART_receive(void) {
	while (!(UCSR0A & _BV(RXC0)));
	return UDR0;
}

void USART_send( unsigned char data) {
	while (!(UCSR0A & _BV(UDRE0)));
	UDR0 = data;
}

void USART_putstring(char *s) {
	while (*s != 0x00) {
		USART_send(*s);
		s++;
	}
	USART_send('\n');
}

int analogRead(uint8_t pin) {
	uint8_t low, high;

	#if defined(ADCSRB) && defined(MUX5)
	// the MUX5 bit of ADCSRB selects whether we're reading from channels
	// 0 to 7 (MUX5 low) or 8 to 15 (MUX5 high).
	ADCSRB = (ADCSRB & ~(1 << MUX5)) | (((pin >> 3) & 0x01) << MUX5);
	#endif

	ADMUX = (1 << 6) | (pin & 0x07);	// start the conversion
	sbi(ADCSRA, ADSC);

	// ADSC is cleared when the conversion finishes
	while (bit_is_set(ADCSRA, ADSC));

	// we have to read ADCL first; doing so locks both ADCL
	// and ADCH until ADCH is read.  reading ADCL second would
	// cause the results of each conversion to be discarded,
	// as ADCL and ADCH would be locked when it completed.
	low  = ADCL;
	high = ADCH;

	return (high << 8) | low;
}