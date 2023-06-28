import os

FLAG = {
    b'\xe5' : 'del',
    b'\x00' : 'end',
    b'\x05' : 'japan'
    b'\x42' : 'last_lfn',
    b'\x44' : 'last_lfn',
}

ATTRIBUTE_MAPPER = {
    b'\x01' : 'Read Only',
    b'\x02' : 'Hidden',
    b'\x04' : 'System',
    b'\x08' : 'Value Label',
    b'\x10' : 'Directory',
    b'\x20' : 'Archive',
    b'\x0f' : 'LFN'
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
        def parse_filename_area(hex_value, first=False):
            name = []
            name.append(hex_value[1:11])
            if first:
                name.append(hex_value[14:22])
            else:
                name.append(hex_value[14:24])
                name.append(hex_value[28:])
            return name
            
        def convert_filename(hex_value):
            name = ''
            for name_ in hex_value:
                for i in range(len(name_)//2):
                    name += chr(int.from_bytes(name_[2*i : 2*(i+1)], byteorder='little'))               
            return name
                
        file_name = parse_filename_area(data[0], first=True)
        file_name = convert_filename(file_name)
        
        for d in data[1:]:
            file_name = convert_filename(parse_filename_area(d)) + file_name
        file_name = file_name.rstrip('\x00')
        return file_name
        

    def sfn_data(self, data):
        def convert_name(name_):
            name = name_.rstrip(b'\x02')
            if name_[:1] in FLAG.keys():
                flag = FLAG[name_[:1]]
                name = name[1:].decode()
            else:
                flag = None
                name = name.decode()
                
            return [flag, name]
        
        def convert_time(self, time_):
            times = {}
            times['date'] = convert_date(time_[-2:])
            try:
                times['time'] = convert_time(time_[-4:-2])
                times['time']['seconds'] += int.from_bytes(time_[-5:-4], byteorder='little')/100
            except:
                pass
                
            return times
            
        meta = data[-1]
        name = meta[:8].rstrip(b'\x02')
        flag, name = convert_name(name)
        ext = meta[8:11].rstrip(b'\x02').decode()
        att = ATTRIBUTE_MAPPER[meta[11:12]]
        c_time = convert_time(meta[13:18])
        a_time = convert_time(meta[18:20])
        w_time = convert_time(meta[22:26])
        sector_start = (int.from_bytes(meta[20:22], byteorder='little') + int.from_bytes(meta[26:28], byteorder='little')) * 8
        file_size = int.from_bytes(meta[28:], byteorder='little')
        
        if len(meta) != 1:
            name, ext = os.path.splitext(self.lfn_data(data[:-1]))
            
        return {
            'name' : name,
            'flag' : flag
            'ext' : ext,
            'att' : att,
            'c_time' : c_time,
            'a_time' : a_time,
            'w_time' : w_time,
            'file_size' : file_size
        }
        
    def DataLoader(self):
        data = []
        data_ = {'flag': None}
        end_flag = True
        for sector_id, data_area in self.data_area:
                
            for i in range(len(data_area)//self.size + 1):
                if data_['flag'] == 'end':
                    break
                if end_flag:
                    data = []
                    
                data.append(self.data_area[i*self.size: (i+1)*self.size])
                end_flag = data[-1][11:12] != b'\x0f'
                if end_flag:
                    data_ = self.sfn_data(data)  
                    data_['sector_start'] += sector_id
                    yield data_
                continue
                
                    