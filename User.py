class User:
    
    def __init__(self, ip_address, port_no, name):
        self.ip_address = ip_address
        self.port_no = port_no
        self.name = name.replace(" ", "")

    def printDetails(self):
        print (self.name, end=" from ")
        print (self.ip_address, end=":")
        print (self.port_no)
    
    def get_address(self):
        return (self.ip_address, self.port_no)