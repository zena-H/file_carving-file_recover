


class Partition:
    def __init__(self, data_file_path):
        self.data_file_path = data_file_path
        self.file = open(self.data_file_path,'rb')
        self.sectors = self.file.read()
        self.sectors = { i : self.sector[i*SECTOR_SIZE : (i+1)*SECTOR_SIZE] for i in range((len(self.sector) + SECTOR_SIZE -1) // SECTOR_SIZE)}
        self.file.close()
        self.my_sector = 0
        self.mbr = self.sectors[self.my_sector = 0]
        self.partition_table = self.mbr[partition_table_start:partition_table_start+48]
        if int.from_bytes(self.partition_table, byteorder='little') == 0:
            # MBR 영역이 손상된 것으로 복구할 것인지 창을 띄우는 것을 구현해야함.
            # 이후에는 VBR 위치 128(보통 128 섹터)을 찾아서 하나씩 찾는 방법을 수행해야함.
            self.partition = None
            
        else:
            self.partition = parse_partition_info()
            
        self.partiton_info = None
        self.partition_data = {'partition_id' : None}
        
        del self.mbr
            
    def parse_partition_info(self, sector_id=0):
        """
        4개의 파티션 테이블 중 선택한 파티션의 정보를 가져옴
        파티션 사이즈는 요즘 chs를 사용하지 않는다하여 lcs 정보만 가져옴
        """
        partition = {}
        for partition_id in range(4):
            partition_info_data = self.partition_table[partition_id * partition_size : (partition_id+1)*partition_table_size]
            if int.from_bytes(partition_info_data, byteorder='little') == 0:
                break
            boot_flag = partition[0] == 128
            partition_type = bytes.fromhex(format(partition[4],'#04x'))
            partition_type = partition_type_mapper[partition_type]
            start_sector = partition_info_data[partition_size['lcs']['start'][0] : partition_size['lcs']['start'][1]]
            sector_size = partition_info_data[partition_size['lcs']['end'][0] : partition_size['lcs']['end'][1]]
            partition[partition_id]= {
                'partition_id'   : partition_id
                'boot_flag'      : boot_flag,
                'partition_type' : partition_type,
                # 실제 partition byte 수는 sector_size * SECTOR_SIZE
                'partition_size'    : int.from_bytes(sector_size, byteorder='little')
                'start_sector'   : int.from_bytes(start_sector, byteorder='little')
            }
        return partition
    def parse_partition_data(self, partition_id):
        if self.parse_partition_info['partition_id'] != partition_id:
            self.partition_info = self.partition[partition_id]
            self.partition_data = self.sectors[self.partition_info['start_sector'] : self.partition_info['start_sector']+self.partition_info['partition_size']])
        
    def recover_partition(self):
    
    
        