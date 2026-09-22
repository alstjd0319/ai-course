class Calculator:
    def __init__(self):
        self._display = "0"
        self._current_num_str = "0"
        self._accumulated_result = 0.0
        self._last_operator = None
        self._is_error = False
        self._after_equal = False
        self._has_decimal = False

    @property
    def display(self):
        return self._display

    def _format_result(self, val: float) -> str:
        rounded = round(val, 10)
        s = format(rounded, '.10f').rstrip('0').rstrip('.')
        if s == "" or s == "-0":
            s = "0"
        return s

    def _reset_state(self, value="0"):
        self._display = value
        self._current_num_str = value
        self._accumulated_result = 0.0
        self._last_operator = None
        self._is_error = False
        self._after_equal = False
        self._has_decimal = False

    def press(self, key: str):
        if self._is_error:
            if key == "C":
                self._reset_state("0")
            return

        if key == "C":
            self._reset_state("0")
            return

        if key == "BS":
            if self._after_equal:
                return
            if self._current_num_str == "0":
                return
            
            new_str = self._current_num_str[:-1]
            if not new_str or new_str == "-":
                new_str = "0"
            elif new_str == ".":
                new_str = "0"
            
            if len(new_str) > 1 and new_str.startswith("0") and new_str[1] != ".":
                new_str = new_str.lstrip("0")
                if not new_str: new_str = "0"

            self._current_num_str = new_str
            self._display = self._current_num_str
            return

        if key == "+/-":
            if self._current_num_str == "0":
                return
            if self._current_num_str.startswith("-"):
                self._current_num_str = self._current_num_str[1:]
            else:
                self._current_num_str = "-" + self._current_num_str
            
            if self._current_num_str == "-":
                self._current_num_str = "0"
            
            temp = self._current_num_str
            if temp.startswith("-"):
                rest = temp[1:]
                if len(rest) > 1 and rest.startswith("0") and rest[1] != ".":
                    self._current_num_str = "-" + rest.lstrip("0")
                    if self._current_num_str == "-": self._current_num_str = "0"
            else:
                if len(temp) > 1 and temp.startswith("0") and temp[1] != ".":
                    self._current_num_str = temp.lstrip("0")
                    if not self._current_num_str: self._current_num_str = "0"

            self._display = self._current_num_str
            return

        if key == "%":
            try:
                val = float(self._current_num_str) / 100.0
                self._current_num_str = self._format_result(val)
                self._display = self._current_num_str
            except ValueError:
                pass
            return

        if key in ("+", "-", "*", "/", "="):
            if key == "=":
                if self._last_operator is None or self._after_equal:
                    return
                self._perform_calculation()
                self._after_equal = True
                return
            else:
                if self._last_operator is None:
                    self._accumulated_result = float(self._current_num_str)
                else:
                    self._perform_calculation()
                
                self._last_operator = key
                self._after_equal = False
                self._current_num_str = "0"
                self._has_decimal = False
                self._display = "0"
                return

        if key.isdigit() or key == ".":
            if self._after_equal:
                self._reset_state("0")
                self._after_equal = False

            if key == ".":
                if self._has_decimal:
                    return
                self._has_decimal = True
                if self._current_num_str == "0":
                    self._current_num_str = "0."
                else:
                    self._current_num_str += "."
            else:
                sig_digits = sum(c.isdigit() for c in self._current_num_str)
                if sig_digits >= 12:
                    return

                if self._current_num_str == "0":
                    self._current_num_str = key
                else:
                    self._current_num_str += key

            if len(self._current_num_str) > 1 and self._current_num_str.startswith("0") and self._current_num_str[1] != ".":
                self._current_num_str = self._current_num_str.lstrip("0")
                if not self._current_num_str or self._current_num_str.startswith("."):
                    self._current_num_str = "0" + self._current_num_str

            self._display = self._current_num_str

    def _perform_calculation(self):
        try:
            val2 = float(self._current_num_str)
            op = self._last_operator
            
            if op == "+":
                res = self._accumulated_result + val2
            elif op == "-":
                res = self._accumulated_result - val2
            elif op == "*":
                res = self._accumulated_result * val2
            elif op == "/":
                if val2 == 0:
                    self._is_error = True
                    self._display = "0으로 나눌 수 없습니다"
                    return
                res = self._accumulated_result / val2
            else:
                res = val2

            self._accumulated_result = res
            self._display = self._format_result(res)
            self._current_num_str = self._display 
            
        except ZeroDivisionError:
            self._is_error = True
            self._display = "0으로 나눌 수 없습니다"
        except Exception:
            pass
