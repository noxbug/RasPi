import RPi.GPIO as GPIO

class Lcd:
    def __init__(self, rs=2, e=3, db7=4, db6=14, db5=15, db4=18):
        """
        Initialize GPIO pin numbers (BCM numbering).
        RS selects register
        0: instruction register
        1: data register
        E starts data read/write
        Rising edge: read RS
        Falling edge: read data bits
        DB7 to DB0 data bits
        """
        self.rs = rs
        self.e = e
        self.db7 = db7
        self.db6 = db6
        self.db5 = db5
        self.db4 = db4
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.rs, self.e, self.db7, self.db6, self.db5, self.db4], GPIO.OUT)

        # Display on/off control
        self.display_on_off = 1
        self.cursor_on_off = 1
        self.cursor_blink = 1

        # Function set
        self.data_length = 0 # 4 bit data length
        self.numer_of_lines = 1 # two display lines
        self.character_font = 0 # 5x8 lines font

    def write_string(self, string):
        for char in string:
            self.write_char(char)

    def write_char(self, char=' '):
        """"Convert char to integer"""
        integer = ord(char)
        self.instruction(integer, True)

    def return_home(self):
        """"Clears entire display and sets DDRAM address 0 in address counter"""
        self.instruction([False, False, False, False, False, False, True])

    def entry_mode_set(self, id=True, s=False):
        """
        Sets cursor move direction and specifies display shift.
        These operations are performed during data write and read.
        I/D = 1: Increment (default)
        I/D = 0: Decrement
        S = 1: Accompanies display shift
        """
        self.instruction([False, False, False, False, False, True, bool(id), bool(s)])

    def display_on_off_control(self, d=True, c=True, b=True):
        """
        Sets entire display (D) on/off,
        cursor on/off (C), and
        blinking of cursor position character (B).
        """
        self.instruction([False, False, False, False, True, bool(d), bool(c), bool(b)])

    def cursor_or_display_shift(self, sc=True, rl=True):
        """
        Moves cursor and shifts display without changing DDRAM contents
        S/C = 1: Display shift (default)
        S/C = 0: Cursor move
        R/L = 1: Shift to the right (default)
        R/L = 0: Shift to the left
        """
        self.instruction([False, False, False, True, bool(sc), bool(rl)])

    def _function_set(self, data_length=self.data_length, number_of_lines=self.number_of_lines, character_font=self.character_font):
        """
        Sets interface data length (DL),
        number of display lines (N),
        and character font (F).
        DL = 1: 8 bits
        DL = 0: 4 bits
        N = 1: 2 lines (default)
        N = 0: 1 line
        F = 1: 5x10 dots
        F = 0: 5x8 dots (default)
        """
        function_set_mask = 32
        data = funtion_set_mask | (data_length << 4) | (number_of_lines << 3) | (character_font << 2)

        self.instruction(data)

    def set_ddram_address(self, address=0,  line=0):
        """
        Sets DDRAM address.
        DDRAM data is sent and
        received after this setting
        address: 0 to 39 dec
        line: 0 or 1
        """
        # instruction bit
        data = [True]
        # select wich line (0/1)
        data.append(bool(line))
        # integer address to binary list
        address_bin = list(map(bool, list(map(int, bin(address)[2:].zfill(6)))))
        data.extend(address_bin)
        self.instruction(data)

    def instruction(self, data, rs=False, data_length=0):
        """
        HD44780U instruction
        RS = 0: Instruction register
        RS = 1: Data register
        DB7 to DB0: Data bits
        """
        GPIO.output(self.rs, rs)
        # higher order bits
        GPIO.output(self.e, True)
        GPIO.output(self.db7, bool((data >> 7) & 1))
        GPIO.output(self.db6, bool((data >> 6) & 1))
        GPIO.output(self.db5, bool((data >> 5) & 1))
        GPIO.output(self.db4, bool((data >> 4) & 1))
        GPIO.output(self.e, False)

        if(data_length == 0):
            # 4 bit data mode
            # lower order bits
            GPIO.output(self.e, True)
            GPIO.output(self.db7, bool((data >> 3) & 1))
            GPIO.output(self.db6, bool((data >> 2) & 1))
            GPIO.output(self.db5, bool((data >> 1) & 1))
            GPIO.output(self.db4, bool(data & 1))
            GPIO.output(self.e, False)

    def cleanup(self):
        """"Clean up all ports"""
        print('GPIO cleanup...')
        GPIO.cleanup()
