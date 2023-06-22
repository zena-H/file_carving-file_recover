import binascii



SECTOR_SIZE = 512

# MBR => 첫번째 섹터
partition_table_size = 16
partition_table_start = 446

partition_size = { 
    "chs" : {
	   "start" : [2,4],
	   "end" : [4,7]
	},
	"lcs" : {
	    "start" : [7,11],
		"end" : [11,15]
	}	
}

partition_type_mapper = { 
    b"\x00" : "Empty",
    b"\x01" : "FAT12 primary partition or logical drive, CHS",
	b"\x04" : "FAT16 partition or logical drive, CHS",
	b"\x05" : "Microsoft Extended partition, CHS",
	b"\x06" : "BIGDOS FAT16 pa띠ion or 1얘ical drive(33MB - 4GB), CHS",
	b"\x07" : "Instaliable FileSystem(NTFS partition or logical drive)",
	b"\x0b" : "FAT32 partition or logical drive, CHS"
	b"\x0C" : "FAT32 partition or logical drive using BIOS INT 13h extensions, LBA",
	b"\x0E" : "BIGDOS FAT16 partition or logical drive using BIOS INT 13h extensions, LBA",
	b"\x0F" : "Extended partition using BIOS INT 13h extensions, LBA",
	b"\x11" : "Hidden FAT12. CHS",
	b"\x14" : "Hidden FAT16. 16MB - 32MB. CHS",
	b"\x16" : "Hidden FAT16. 32MB - 2GB. CHS",
	b"\x1b" : "Hidden FAT32, CHS",
	b"\x1C" : "Hidden FAT32. LBA",
	b"\x1E" : "Hidden FAT16, 32MB - 2GB, LBA",
	b"\x42" : "Microsoft MBR, Dynamic Disk",
	b"\x82" : "Solaris x86",
	b"\x82" : "Linux Swap",
	b"\x83" : "Linux",
	b"\x84" : "Hibernation",
	b"\x85" : "Linux Extended",
	b"\x86" : "NTFS Volume Set",
	b"\x87" : "NTFS Volume Set",
	b"\xA0" : "Hibernation",
	b"\xA1" : "Hibernation",
	b"\xA5" : "FreeBSD",
	b"\xA6" : "OpenBSD",
	b"\xA8" : "MacOS X",
	b"\xA9" : "NetBSD",
	b"\xAb" : "MacOS X Boot",
	b"\xB7" : "BSDI",
	b"\xB8" : "BSDI swap",
	b"\xEE" : "EFI GPT Disk",
	b"\xEF" : "EFI System Partition",
	b"\xFb" : "Vmware FileSystem",
	b"\xFC" : "Vmware swap"
}

def hexbinary_to_int(binary_str):
    hex_str = binary_str[::-1]
    hex_str = binascii.hexlify(hex_str)
    return int(hex_str,16)
    
   