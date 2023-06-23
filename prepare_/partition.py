


class Partition:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.file = open(self.data_file_path,'rb')
        self.mbr = self.file.read(SECTOR_SIZE)
        self.partition_table = self.mbr[partition_table_start:partition_table_start+48]
        if hexbinary_to_int(self.partition_table) == 0:
            # MBR 영역이 손상된 것으로 복구할 것인지 창을 띄우는 것을 구현해야함.
            # 이후에는 VBR 위치 128(보통 128 섹터)을 찾아서 하나씩 찾는 방법을 수행해야함.
            self.partition = None
            
        else:
            self.partition = {
                '0' : parse_partition_info(partition_id=0),
                '1' : parse_partition_info(partition_id=1),
                '2' : parse_partition_info(partition_id=2),
                '3' : parse_partition_info(partition_id=3)
               }
        self.partition_data = None
        
        del self.mbr
            
    def parse_partition_info(self, partition_id=0):
        """
        4개의 파티션 테이블 중 선택한 파티션의 정보를 가져옴
        파티션 사이즈는 요즘 chs를 사용하지 않는다하여 lcs 정보만 가져옴
        """
        partition_info_data = self.partition_table[partition_id * partition_size : (partition_id+1)*partition_table_size]
        if hexbinary_to_int(partition_info_data) == 0:
            return {
                'partition_id'   : partition_id
                'boot_flag'      : None,
                'partition_type' : None,
                'sector_size'    : None,
                'start_sector'   : None
            }
        boot_flag = partition[0] == 128
        partition_type = bytes.fromhex(format(partition[4],'#04x'))
        partition_type = partition_type_mapper[partition_type]
        start_sector = partition_info_data[partition_size['lcs']['start'][0] : partition_size['lcs']['start'][1]]
        sector_size = partition_info_data[partition_size['lcs']['end'][0] : partition_size['lcs']['end'][1]]
        return {
            'partition_id'   : partition_id
            'boot_flag'      : boot_flag,
            'partition_type' : partition_type,
            'sector_size'    : hexbinary_to_int(sector_size) * SECTOR_SIZE
            'start_sector'   : hexbinary_to_int(start_sector)
        }
        
    def parse_partition_data(self, partition_id):
        self.partition_info = self.partition[partition_id]
        self.file.read(self.partition_info['start_sector'] * SECTOR_SIZE)
        self.partition_data = self.file.read(self.partition_info['sector_size'])
        
    
    def chg_partition(self, partition_id):
        self.file = open(self.data_file_path,'rb')
        self.mbr = self.file.read(SECTOR_SIZE)
        self.partition_data = None
        