FLAG = {
    
}

ATTRIBUTE_MAPPER = {
    
}

def convert_date(hex_value):
    date = bin(int.from_bytes(byt, byteorder='little'))[2:].zfill(16)
    year = 1980 + int(date[:7], 2)
    month = int(date[7:11], 2)
    day = int(date[11:], 2)
    return {
            'year' : year,
            'month', : month,
            'day' : day
        }
        
def convert_time(hex_value):
    date = bin(int.from_bytes(byt, byteorder='little'))[2:].zfill(16)
    hour = int(date[:5], 2)
    month = int(date[5:11], 2)
    day = int(date[11:], 2)
    return {
            'hour' : hour,
            'minutes', : minutes,
            'seconds' : seconds
        

class DATA_AREA:
    def __init__(self, data_area):
        self.data_area = data_area
        self.size = 32
        
    def lfn_data(self, data):
        
    def sfn_data(self, data):
        def convert_name(name_):
            if name_[:1] in FLAG:
                flag = FLAG[name_[:1]]
                name = name_[1:].rstrip(b'\x02').decode()
            else:
                flag = None
                name = name_.rstrip(b'\x02').decode()
                
            return {
                    'flag' : flag
                    'name' : name
                    }
                    
        meta = data[-1]
        name = meta[:8].rstrip(b'\x02')
        name = convert_name(name)
#        ext = meta[8:11].rstrip(b'\x02').decode()
        att = meta[11:12]
#        c_time = meta[13:18]
#        a_time = meta[18:20]
#        w_time = meta[22:26]
        file_size = int.from_bytes(meta[28:], byteorder='little')
        
    def DataLoader(self):
        data = []
        end_flag = True
        for i in range(len(self.data_area)//self.size + 1):
            if end_flag:
                data = []
                
            data.append(self.data_area[i*self.size: (i+1)*self.size])
            end_flag = data[11:12] != b'\x0f'
            if end_flag:
                yield data
            continue
            
                