class Message:
    def __init__(self,data_source = ""):
        self.data_source = data_source
        self.repairs = []
        self.errors = []

    def append_repairs(self,message):
        self.repairs.append(message)
    
    def append_errors(self,message):
        self.errors.append(message)

    def return_list(self):
        return ["Registros con errores y reparados: \n"] + self.repairs + ["Registros con errores y rechazados: \n"] + self.errors