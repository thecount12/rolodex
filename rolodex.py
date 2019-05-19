"""
parsing rolodex csv information
"""
import json


class Rolodex(object):
    """
    usage: output = Rolodex('file.csv')
           output.format_output()
    """

    def __init__(self, file_name):
        """
        Args:
            file_name: string
        """
        self.file_name = file_name
        self.my_list = []
        self.my_num = []
        self.number = 0

    def input_data(self):
        """
        Returns: list
        """
        with open(self.file_name, 'r') as input_file:
            rolodex_data = input_file.readlines()
        return rolodex_data

    @staticmethod
    def name_check(name):
        """
        Args:
            name: string
        Returns: tuple
        """
        test_name = name.split(" ")
        if len(test_name) == 2:
            return test_name[0], test_name[1]
        else:
            middle = "{0} {1}".format(test_name[0], test_name[1])
            return middle, test_name[2]

    @staticmethod
    def _digits(data):
        """
        Args:
            data: string
        Returns: boolean
        """
        if data.split(" ") != 4:
            try:
                data = int(data)
            except ValueError:
                pass
            return isinstance(data, int)

    def find(self, data):
        """
        Args:
            data: list
        Returns: tuple
        """
        zip_code = phone = color = ""
        for _, line in enumerate(data):
            if self._digits(line):
                zip_code = line
            if "(" in line:
                phone = line.replace("(", "").replace(")", "")
            if len(line.split(" ")) == 4:
                phone = line.strip().replace(" ", "-")
            if len(line.split(" ")) != 4 and "(" not in line and not self._digits(line):
                color = line
        return zip_code, phone, color

    def build_dict(self, dat0, dat1, dat2, dat3, dat4):
        """
        Args:
            dat0: str() firstname
            dat1: str() lastname
            dat2: str() zipcode
            dat3: str() phonenumber
            dat4: str() color
        Returns: dict()
        """
        my_dict = dict()
        if len(self.find([dat2, dat3, dat4])[0].strip()) > 5 or len(self.find([dat2, dat3, dat4])[1].strip()) > 14:
            my_dict["Error"] = "Error"
            self.my_num.append(self.number)
        else:
            my_dict["firstname"] = dat0
            my_dict["lastname"] = dat1
            my_dict["zipcode"] = self.find([dat2, dat3, dat4])[0].strip()
            my_dict["phonenumber"] = self.find([dat2, dat3, dat4])[1].strip()
            my_dict["color"] = self.find([dat2, dat3, dat4])[2].strip()
        return my_dict

    def validate_fields(self):
        """
        Returns: list() of dictionary that is sanitized
        """
        for _, line in enumerate(self.input_data()):
            x = line.split(",")
            if len(x) == 4:
                a_dict = self.build_dict(self.name_check(x[0])[0].strip(), self.name_check(x[0])[1].strip(),
                                         x[1], x[2], x[3])
            if len(x) == 5:
                a_dict = self.build_dict(x[0].strip(), x[1].strip(), x[2], x[3], x[4])
            if len(x) == 1:
                # a_dict["Error"] = "Error"
                self.my_num.append(self.number)
            self.number += 1
            if len(a_dict) > 1:
                self.my_list.append(a_dict)
        # fixed but might change logic
        return [dict(t) for t in {tuple(d.items()) for d in self.my_list}]

    def format_output(self):
        """
        prints json format output with indent and keys sorted
        """
        boom = dict()
        boom["entries"] = self.validate_fields()
        boom["errors"] = self.my_num
        print(json.dumps(boom, indent=1, sort_keys=True))


if __name__ == "__main__":
    test_output = Rolodex('data.csv')
    test_output.format_output()
