# tape.py

class Tape:
    def __init__(self, input_string, blank_symbol='_'):
        """
        Inicializa la cinta con la cadena de entrada y configura el cabezal al inicio.

        :param input_string: Cadena de entrada para la cinta.
        :param blank_symbol: Símbolo que representa el blanco en la cinta.
        """
        self.blank_symbol = blank_symbol
        self.tape = list(input_string)
        self.head = 0  # Posición inicial del cabezal

    def read(self):
        """
        Lee el símbolo bajo el cabezal.

        :return: Símbolo en la posición actual del cabezal.
        """
        if self.head < 0 or self.head >= len(self.tape):
            return self.blank_symbol
        return self.tape[self.head]

    def write(self, symbol):
        """
        Escribe un símbolo en la posición del cabezal.

        :param symbol: Símbolo a escribir.
        """
        if self.head < 0:
            # Extender la cinta hacia la izquierda
            num_blanks = abs(self.head)
            self.tape = [self.blank_symbol] * num_blanks + self.tape
            self.head = 0
        elif self.head >= len(self.tape):
            # Extender la cinta hacia la derecha
            num_blanks = self.head - len(self.tape) + 1
            self.tape.extend([self.blank_symbol] * num_blanks)

        self.tape[self.head] = symbol

    def move(self, direction):
        """
        Mueve el cabezal en la dirección indicada.

        :param direction: 'L' para izquierda, 'R' para derecha, 'S' para quedarse en el mismo lugar.
        """
        if direction == 'L':
            self.head -= 1
        elif direction == 'R':
            self.head += 1
        elif direction == 'S':
            pass  # El cabezal no se mueve
        else:
            raise ValueError(f"Dirección de movimiento inválida: '{direction}'.")

    def get_tape_contents(self):
        """
        Devuelve una representación de la cinta como cadena.

        :return: Cadena que representa el contenido de la cinta.
        """
        return ''.join(self.tape)

    def get_head_position(self):
        """
        Devuelve la posición actual del cabezal.

        :return: Índice del cabezal en la cinta.
        """
        return self.head
