#!/usr/bin/env python

import os
import re
import pickle
from time import sleep
from subprocess import Popen, PIPE, STDOUT, call

tmp = "/tmp/.gbi/"
if not os.path.exists(tmp):
    os.makedirs(tmp)
installer = "/usr/local/lib/gbi/"
sysinstall = "/usr/local/sbin/pc-sysinstall"
partitiondb = "%spartitiondb/" % tmp
query = "sh /usr/local/lib/gbi/backend-query/"
query_disk = '%sdisk-list.sh' % query
detect_sheme = '%sdetect-sheme.sh' % query
diskdb = "%sdisk" % partitiondb
query_partition = '%sdisk-part.sh' % query
query_label = '%sdisk-label.sh' % query
disk_info = '%sdisk-info.sh' % query
nl = "\n"
memory = 'sysctl hw.physmem'
disk_file = '%sdisk' % tmp
dslice = '%sslice' % tmp
Part_label = '%spartlabel' % tmp
part_schem = '%sscheme' % tmp
boot_file = '%sboot' % tmp
disk_db_file = f'{tmp}disk.db'


def disk_database():
    df = open(disk_db_file, 'rb')
    dl = pickle.load(df)
    return dl


def zfs_disk_query():
    disk_output = Popen(sysinstall + " disk-list", shell=True, stdin=PIPE,
                        stdout=PIPE, universal_newlines=True, close_fds=True)
    return disk_output.stdout.readlines()


def zfs_disk_size_query(disk):
    disk_info_output = Popen(sysinstall + " disk-info " + disk, shell=True,
                             stdin=PIPE, stdout=PIPE, universal_newlines=True,
                             close_fds=True)
    return disk_info_output.stdout.readlines()[3].partition('=')[2]


def how_partition(disk):
    partitions = disk_database()[disk]['partitions']
    if partitions is None:
        return 0
    else:
        return len(partitions)


def get_disk_from_partition(part):
    if set("p") & set(part):
        return part.partition('p')[0]
    else:
        return part.partition('s')[0]


def slice_number(part):
    if set("p") & set(part):
        return int(part.partition('p')[2])
    else:
        return int(part.partition('s')[2])


class create_disk_partition_db():

    def disk_list(self):
        cmd = 'sysctl -n kern.disks'
        disk_Popen = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
                           universal_newlines=True, close_fds=True)
        disks = disk_Popen.stdout.read()
        cleaned_disk = re.sub(r'acd[0-9]*|cd[0-9]*|scd[0-9]*', '', disks)
        return sorted(cleaned_disk.split())

    def device_model(self, disk):
        cmd = f"diskinfo -v {disk} 2>/dev/null | grep 'Disk descr' | cut -d '#' -f1 | tr -d '\t'"
        disk_Popen = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
                           universal_newlines=True, close_fds=True)
        return disk_Popen.stdout.read().strip()

    def disk_size(self, disk):
        cmd = "%s %s" % (disk_info, disk)
        ds = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
                   universal_newlines=True, stderr=STDOUT, close_fds=True)
        diskSize = ds.stdout.readlines()[0].rstrip()
        return diskSize

    def find_Scheme(self, disk):
        cmd = "%s %s" % (detect_sheme, disk)
        shm_out = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
                        universal_newlines=True, stderr=STDOUT, close_fds=True)
        scheme = shm_out.stdout.readlines()[0].rstrip()
        return scheme

    def mbr_partition_slice_db(self, disk):
        partition_output = Popen('%s %s' % (query_partition, disk),
                                 shell=True, stdin=PIPE, stdout=PIPE,
                                 universal_newlines=True)
        slice_db = {}
        free_num = 1
        for line in partition_output.stdout:
            info = line.strip().split()
            slice_name = info[0]
            if 'freespace' in line:
                slice_name = f'freespace{free_num}'
                free_num += 1
            partition_db = self.mbr_partition_db(info[0])
            # partition_list = [] if partition_db is None else list(partition_db.keys())
            partitions = {
                'name': slice_name,
                'size': info[1].partition('M')[0],
                'mount_point': '',
                'file_system': info[2],
                'stat': None,
                'partitions': partition_db,
                'partition_list': [] if partition_db is None else list(partition_db.keys())
            }
            slice_db[slice_name] = partitions
        return slice_db

    def mbr_partition_db(self, pslice):
        if 'freespace' in pslice:
            return None
        else:
            slice_output = Popen('%s %s' % (query_label, pslice), shell=True,
                                 stdin=PIPE, stdout=PIPE,
                                 universal_newlines=True)
            partition_db = {}
            alph = ord('a')
            free_num = 1
            for line in slice_output.stdout:
                info = line.strip().split()
                if 'freespace' in line:
                    partition_name = f'freespace{free_num}'
                    free_num += 1
                else:
                    letter = chr(alph)
                    partition_name = f'{info[0]}{letter}'
                    alph += 1
                partitions = {
                    'name': partition_name,
                    'size': info[1].partition('M')[0],
                    'mount_point': '',
                    'file_system': info[2],
                    'stat': None,
                }
                partition_db[partition_name] = partitions
            if not partition_db:
                return None
            return partition_db

    def gpt_partition_db(self, disk):
        partition_output = Popen('%s %s' % (query_partition, disk),
                                 shell=True, stdin=PIPE, stdout=PIPE,
                                 universal_newlines=True)
        partition_db = {}
        free_num = 1
        for line in partition_output.stdout:
            info = line.strip().split()
            slice_name = info[0]
            if 'freespace' in line:
                slice_name = f'freespace{free_num}'
                free_num += 1
            partitions = {
                'name': info[0],
                'size': info[1].partition('M')[0],
                'mount_point': '',
                'file_system': info[2],
                'stat': None,
                'partitions': None,
                'partition_list': []
            }
            partition_db[slice_name] = partitions
        return partition_db

    def __init__(self):
        if os.path.exists(disk_db_file):
            os.remove(disk_db_file)
        df = open(disk_db_file, 'wb')
        disk_db = {}
        for disk in self.disk_list():
            disk_info_db = {}
            if self.find_Scheme(disk) == "GPT":
                disk_info_db['scheme'] = 'GPT'
                partition_db = []
                partition_db = self.gpt_partition_db(disk)
            elif self.find_Scheme(disk) == "MBR":
                disk_info_db['scheme'] = 'MBR'
                partition_db = self.mbr_partition_slice_db(disk)
            else:
                disk_info_db['scheme'] = None
                partition_db = None
            disk_info_db['size'] = self.disk_size(disk)
            disk_info_db['device_model'] = self.device_model(disk)
            disk_info_db['partitions'] = partition_db
            disk_info_db['partition_list'] = [] if partition_db is None else list(partition_db.keys())
            disk_info_db['stat'] = None
            disk_db[disk] = disk_info_db
        # print(json.dumps(disk_db, indent=4))
        pickle.dump(disk_db, df)
        df.close()


def diskSchemeChanger(scheme, path, disk, size):
    disk_data = disk_database()
    if scheme is None:
        disk_data[disk]['scheme'] = 'GPT'
    else:
        disk_data[disk]['scheme'] = scheme
    dsl = []
    mdsl = []
    if os.path.exists(tmp + 'destroy'):
        df = open(tmp + 'destroy', 'rb')
        mdsl = pickle.load(df)
    dsl.extend(([disk, scheme]))
    mdsl.append(dsl)
    cf = open(tmp + 'destroy', 'wb')
    pickle.dump(mdsl, cf)
    cf.close()
    if disk_data[disk]['partitions'] is None:
        disk_data[disk]['partitions'] = {
            'freespace1': {
                'name': 'freespace1',
                'size': size,
                'mount_point': '',
                'file_system': 'none',
                'stat': None,
                'partitions': None,
                'partition_list': []
            }
        }
        disk_data[disk]['partition_list'] = [
            'freespace1'
        ]
    df = open(disk_db_file, 'wb')
    pickle.dump(disk_data, df)
    df.close()


def find_next_partition(partition_name, partition_list):
    for num in range(1, 10000):
        if f'{partition_name}{num}' not in partition_list:
            return f'{partition_name}{num}'


class Delete_partition():

    def find_if_label(self, part):
        last = part[-1]
        if re.search('[a-z]', last):
            return True

    def delete_label(self, part, spart, path):
        disk_data = disk_database()
        llist = open(partitiondb + spart, 'rb')
        ll = pickle.load(llist)
        last_num = len(ll) - 1
        lnum = path[2]
        if last_num == lnum:
            free = int(ll[last_num][1])
            if lnum != 0 and ll[lnum - 1][0] == 'freespace':
                free = free + int(ll[lnum - 1][1])
                ll[lnum] = ['freespace', free, '', '']
                ll.remove(ll[lnum - 1])
            else:
                ll[lnum] = ['freespace', free, '', '']
        elif lnum == 0:
            free = int(ll[lnum][1])
            if ll[lnum + 1][0] == 'freespace':
                free = free + int(ll[lnum + 1][1])
                ll.remove(ll[lnum + 1])
            ll[lnum] = ['freespace', free, '', '']
        else:
            free = int(ll[lnum][1])
            if ll[lnum + 1][0] == 'freespace':
                free = free + int(ll[lnum + 1][1])
                ll.remove(ll[lnum + 1])
            if lnum != 0 and ll[lnum - 1][0] == 'freespace':
                free = free + int(ll[lnum - 1][1])
                ll[lnum] = ['freespace', free, '', '']
                ll.remove(ll[lnum - 1])
            else:
                ll[lnum] = ['freespace', free, '', '']
        savepl = open(partitiondb + spart, 'wb')
        pickle.dump(ll, savepl)
        savepl.close()
        df = open(disk_db_file, 'wb')
        pickle.dump(disk_data, df)
        df.close()

        llist = open(partitiondb + spart, 'rb')
        lablelist = pickle.load(llist)
        pfile = open(Part_label, 'w')
        for partlist in lablelist:
            if partlist[2] != '':
                pfile.writelines('%s %s %s\n' % (partlist[3], partlist[1],
                                                 partlist[2]))
        pfile.close()

    def __init__(self, part, path):
        if part == "freespace":
            pass
        elif self.find_if_label(part) is True:
            spart = part[:-1]
            self.delete_label(part, spart, path)
        else:
            drive = get_disk_from_partition(part)
            self.delete_slice(drive, part, path)

    def delete_slice(self, drive, partition, path):
        disk_data = disk_database()
        partitions_info = disk_data[drive]['partitions']
        partition_list = disk_data[drive]['partition_list']
        last_list_number = len(partition_list) - 1
        store_list_number = path[1]
        size_free = int(partitions_info[partition]['size'])
        if last_list_number == store_list_number and len(partition_list) > 1:
            partition_behind = partition_list[store_list_number - 1]
            if 'freespace' in partition_behind:
                size_free += int(partitions_info[partition_behind]['size'])
                partition_list.remove(partition)
                disk_data[drive]['partitions'].pop(partition, None)
                disk_data[drive]['partitions'][partition_behind] = {
                    'name': partition_behind,
                    'size': size_free,
                    'mount_point': '',
                    'file_system': 'none',
                    'stat': None,
                    'partitions': None,
                    'partition_list': []
                }
                disk_data[drive]['partition_list'] = partition_list
            else:
                free_name = find_next_partition('freespace', partition_list)
                partition_list[store_list_number] = free_name
                disk_data[drive]['partitions'].pop(partition, None)
                disk_data[drive]['partitions'][free_name] = {
                    'name': free_name,
                    'size': size_free,
                    'mount_point': '',
                    'file_system': 'none',
                    'stat': None,
                    'partitions': None,
                    'partition_list': []
                }
                disk_data[drive]['partition_list'] = partition_list
        elif store_list_number == 0 and len(partition_list) > 1:
            partition_after = partition_list[store_list_number + 1]
            if 'freespace' in partition_after:
                size_free += int(partitions_info[partition_after]['size'])
                partition_list.remove(partition)
                disk_data[drive]['partitions'].pop(partition, None)
                disk_data[drive]['partitions'][partition_after] = {
                    'name': partition_after,
                    'size': size_free,
                    'mount_point': '',
                    'file_system': 'none',
                    'stat': None,
                    'partitions': None,
                    'partition_list': []
                }
                disk_data[drive]['partition_list'] = partition_list
            else:
                free_name = find_next_partition('freespace', partition_list)
                partition_list[store_list_number] = free_name
                disk_data[drive]['partitions'].pop(partition, None)
                disk_data[drive]['partitions'][free_name] = {
                    'name': free_name,
                    'size': size_free,
                    'mount_point': '',
                    'file_system': 'none',
                    'stat': None,
                    'partitions': None,
                    'partition_list': []
                }
                disk_data[drive]['partition_list'] = partition_list
        elif len(partition_list) > 2:
            partition_behind = partition_list[store_list_number - 1]
            partition_after = partition_list[store_list_number + 1]
            size_behind = int(partitions_info[partition_behind]['size'])
            size_after = int(partitions_info[partition_after]['size'])
            if 'freespace' in partition_behind and 'freespace' in partition_after:
                size_free += size_behind + size_after
                partition_list.remove(partition)
                partition_list.remove(partition_after)
                disk_data[drive]['partitions'].pop(partition, None)
                disk_data[drive]['partitions'][partition_behind] = {
                    'name': partition_behind,
                    'size': size_free,
                    'mount_point': '',
                    'file_system': 'none',
                    'stat': None,
                    'partitions': None,
                    'partition_list': []
                }
                disk_data[drive]['partition_list'] = partition_list
            elif 'freespace' in partition_behind:
                size_free += size_behind
                partition_list.remove(partition)
                disk_data[drive]['partitions'].pop(partition, None)
                disk_data[drive]['partitions'][partition_behind] = {
                    'name': partition_behind,
                    'size': size_free,
                    'mount_point': '',
                    'file_system': 'none',
                    'stat': None,
                    'partitions': None,
                    'partition_list': []
                }
                disk_data[drive]['partition_list'] = partition_list
            elif 'freespace' in partition_after:
                size_free += size_after
                partition_list.remove(partition)
                disk_data[drive]['partitions'].pop(partition, None)
                disk_data[drive]['partitions'][partition_after] = {
                    'name': partition_after,
                    'size': size_free,
                    'mount_point': '',
                    'file_system': 'none',
                    'stat': None,
                    'partitions': None,
                    'partition_list': []
                }
                disk_data[drive]['partition_list'] = partition_list
            else:
                free_name = find_next_partition('freespace', partition_list)
                partition_list[store_list_number] = free_name
                disk_data[drive]['partitions'].pop(partition, None)
                disk_data[drive]['partitions'][free_name] = {
                    'name': free_name,
                    'size': size_free,
                    'mount_point': '',
                    'file_system': 'none',
                    'stat': None,
                    'partitions': None,
                    'partition_list': []
                }
                disk_data[drive]['partition_list'] = partition_list
        else:
            free_name = find_next_partition('freespace', partition_list)
            partition_list[store_list_number] = free_name
            disk_data[drive]['partitions'].pop(partition, None)
            disk_data[drive]['partitions'][free_name] = {
                'name': free_name,
                'size': size_free,
                'mount_point': '',
                'file_system': 'none',
                'stat': None,
                'partitions': None,
                'partition_list': []
            }
            disk_data[drive]['partition_list'] = partition_list

        disk_db = open(disk_db_file, 'wb')
        pickle.dump(disk_data, disk_db)
        disk_db.close()

        # if delete file exist check if slice is in the list
        if os.path.exists(tmp + 'delete'):
            df = open(tmp + 'delete', 'rb')
            main_delete_list = pickle.load(df)
            if partition not in main_delete_list:
                main_delete_list.append(partition)
        else:
            main_delete_list = [partition]
        cf = open(tmp + 'delete', 'wb')
        pickle.dump(main_delete_list, cf)
        cf.close()

        if "p" in partition:
            new_partitions = open(Part_label, 'w')
            for part in partition_list:
                partitions_info = disk_data[drive]['partitions']
                size = partitions_info[part]['size']
                mount_point = partitions_info[part]['mount_point']
                file_system = partitions_info[part]['file_system']
                stat = partitions_info[part]['stat']
                if stat == 'new':
                    new_partitions.writelines(f'{file_system} {size} {mount_point}\n')
            new_partitions.close()


class autoDiskPartition():

    def delete_mbr_partition(self, disk):
        plist = partition_query(disk)
        for part in plist:
            if part[0] == 'freespace':
                pass
            else:
                os.remove(partitiondb + part[0])

    def create_mbr_partiton(self, disk, size):
        file_disk = open(disk_file, 'w')
        file_disk.writelines('%s\n' % disk)
        file_disk.close()
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=MBR')
        sfile.close()
        plist = []
        mplist = []
        dpsf = open(partitiondb + disk, 'wb')
        plist.extend((disk + "s1", size, '', 'freebsd'))
        mplist.append(plist)
        pickle.dump(mplist, dpsf)
        dpsf.close()
        number = int(size.partition('M')[0])
        slice_file = open(dslice, 'w')
        slice_file.writelines('all\n')
        slice_file.writelines('%s\n' % number)
        slice_file.close()
        # ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
        #             universal_newlines=True, close_fds=True)
        # mem = ram.stdout.read()
        # swap = int(int(mem.partition(':')[2].strip()) / (1024 * 1024))
        swap = 2048
        rootNum = int(number - swap)
        llist = []
        mllist = []
        plf = open(partitiondb + disk + 's1', 'wb')
        llist.extend(([disk + 's1a', rootNum, '/', 'UFS+SUJ']))
        mllist.append(llist)
        llist = []
        llist.extend(([disk + 's1b', swap, 'none', 'SWAP']))
        mllist.append(llist)
        pickle.dump(mllist, plf)
        plf.close()
        pfile = open(Part_label, 'w')
        pfile.writelines('UFS+SUJ %s /\n' % rootNum)
        pfile.writelines('SWAP 0 none\n')
        pfile.close()

    def __init__(self, disk, size, scheme):
        self.bios_type = bios_or_uefi()
        if scheme == 'GPT':
            self.create_gpt_partiton(disk, size)
        elif scheme == 'MBR':
            if os.path.exists(partitiondb + disk):
                self.delete_mbr_partition(disk)
            self.create_mbr_partiton(disk, size)

    def create_gpt_partiton(self, disk, size):
        file_disk = open(disk_file, 'w')
        file_disk.writelines('%s\n' % disk)
        file_disk.close()
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=GPT')
        sfile.close()
        number = int(size.partition('M')[0])
        slice_file = open(dslice, 'w')
        slice_file.writelines('all\n')
        slice_file.writelines('%s\n' % number)
        slice_file.close()
        # ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
        #             universal_newlines=True, close_fds=True)
        # mem = ram.stdout.read()
        # swap = int(int(mem.partition(':')[2].strip()) / (1024 * 1024))
        swap = 2048
        if self.bios_type == "UEFI":
            bnum = 256
        else:
            bnum = 1
        rootNum = int(number - swap)
        rnum = int(rootNum - bnum)
        plist = []
        mplist = []
        plf = open(partitiondb + disk, 'wb')
        if self.bios_type == "UEFI":
            plist.extend(([disk + 'p1', bnum, 'none', 'UEFI']))
        else:
            plist.extend(([disk + 'p1', bnum, 'none', 'BOOT']))
        mplist.append(plist)
        plist = []
        plist.extend(([disk + 'p2', rnum, '/', 'UFS+SUJ']))
        mplist.append(plist)
        plist = []
        plist.extend(([disk + 'p3', swap, 'none', 'SWAP']))
        mplist.append(plist)
        pickle.dump(mplist, plf)
        plf.close()
        pfile = open(Part_label, 'w')
        if self.bios_type == "UEFI":
            pfile.writelines('UEFI %s none\n' % bnum)
        else:
            pfile.writelines('BOOT %s none\n' % bnum)
        pfile.writelines('UFS+SUJ %s /\n' % rnum)
        pfile.writelines('SWAP 0 none\n')
        pfile.close()


class autoFreeSpace():

    def create_mbr_partiton(self, disk, size, sl, path, fs):
        file_disk = open(disk_file, 'w')
        file_disk.writelines('%s\n' % disk)
        file_disk.close()
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=MBR')
        sfile.close()
        plist = []
        mplist = partition_query(disk)
        dpsf = open(partitiondb + disk, 'wb')
        plist.extend((disk + "s%s" % sl, size, '', 'freebsd'))
        mplist[path] = plist
        pickle.dump(mplist, dpsf)
        dpsf.close()
        number = int(size)
        slice_file = open(dslice, 'w')
        slice_file.writelines('s%s\n' % sl)
        slice_file.writelines('%s\n' % number)
        slice_file.close()
        # ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
        #             universal_newlines=True, close_fds=True)
        # mem = ram.stdout.read()
        # swap = int(int(mem.partition(':')[2].strip()) / (1024 * 1024))
        swap = 2048
        rootNum = int(number - swap)
        llist = []
        mllist = []
        plf = open(partitiondb + disk + 's%s' % sl, 'wb')
        if fs == "ZFS":
            layout = "/(compress=lz4|atime=off),/root(compress=lz4)," \
                "/tmp(compress=lz4),/usr(canmount=off|mountpoint=none)," \
                "/usr/home(compress=lz4),/usr/jails(compress=lz4)," \
                "/usr/obj(compress=lz4),/usr/ports(compress=lz4)," \
                "/usr/src(compress=lz4)," \
                "/var(canmount=off|atime=on|mountpoint=none)," \
                "/var/audit(compress=lz4),/var/log(compress=lz4)," \
                "/var/mail(compress=lz4),/var/tmp(compress=lz4)"
        else:
            layout = '/'
        llist.extend(([disk + 's%sa' % sl, rootNum, layout, fs]))
        mllist.append(llist)
        llist = []
        llist.extend(([disk + 's%sb' % sl, swap, 'none', 'SWAP']))
        mllist.append(llist)
        pickle.dump(mllist, plf)
        plf.close()
        pfile = open(Part_label, 'w')
        pfile.writelines(f'{fs} {rootNum} {layout}\n')
        pfile.writelines('SWAP %s none\n' % int(swap - 1))
        pfile.close()
        pl = []
        mpl = []
        if os.path.exists(tmp + 'create'):
            pf = open(tmp + 'create', 'rb')
            mpl = pickle.load(pf)
        pl.extend(([disk + "s%s" % sl, size]))
        mpl.append(pl)
        cf = open(tmp + 'create', 'wb')
        pickle.dump(mpl, cf)
        cf.close()

    def __init__(self, path, size, fs, efi_exist, disk, scheme):
        self.bios_type = bios_or_uefi()
        sl = path[1] + 1
        lv = path[1]
        if scheme == "GPT":
            self.create_gpt_partiton(disk, size, sl, lv, fs, efi_exist)
        elif scheme == "MBR":
            self.create_mbr_partiton(disk, size, sl, lv, fs)

    def create_gpt_partiton(self, disk, size, sl, path, fs, efi_exist):
        file_disk = open(disk_file, 'w')
        file_disk.writelines('%s\n' % disk)
        file_disk.close()
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=GPT')
        sfile.close()
        number = int(size.partition('M')[0])
        # number = number - 512
        # ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
        #             universal_newlines=True, close_fds=True)
        # mem = ram.stdout.read()
        # swap = int(int(mem.partition(':')[2].strip()) / (1024 * 1024))
        swap = 2048
        rootNum = int(number - swap)
        if self.bios_type == "UEFI" and efi_exist is False:
            bs = 256
        elif self.bios_type == "BOOT":
            bs = 1
        else:
            bs = 0
        rootNum = int(rootNum - bs)
        plist = []
        mplist = partition_query(disk)
        plf = open(partitiondb + disk, 'wb')
        done = False
        if self.bios_type == "UEFI" and efi_exist is False:
            plist.extend(([disk + 'p%s' % sl, bs, 'none', 'UEFI']))
            rsl = int(sl + 1)
            swsl = int(rsl + 1)
        elif self.bios_type == "BOOT":
            plist.extend(([disk + 'p%s' % sl, bs, 'none', 'BOOT']))
            rsl = int(sl + 1)
            swsl = int(rsl + 1)
        else:
            rsl = int(sl)
            swsl = int(rsl + 1)

        if len(plist) != 0:
            done = True
            mplist[path] = plist
            plist = []

        if fs == "ZFS":
            layout = "/(compress=lz4|atime=off),/root(compress=lz4)," \
                "/tmp(compress=lz4),/usr(canmount=off|mountpoint=none)," \
                "/usr/home(compress=lz4),/usr/jails(compress=lz4)," \
                "/usr/obj(compress=lz4),/usr/ports(compress=lz4)," \
                "/usr/src(compress=lz4)," \
                "/var(canmount=off|atime=on|mountpoint=none)," \
                "/var/audit(compress=lz4),/var/log(compress=lz4)," \
                "/var/mail(compress=lz4),/var/tmp(compress=lz4)"
        else:
            layout = '/'
        plist.extend(([disk + 'p%s' % rsl, rootNum, layout, fs]))
        if done is False:
            mplist[path] = plist
        else:
            mplist.insert(rsl - 1, plist)
        plist = []
        plist.extend(([disk + 'p%s' % swsl, swap, 'none', 'SWAP']))
        mplist.insert(swsl - 1, plist)
        pickle.dump(mplist, plf)
        plf.close()
        slice_file = open(dslice, 'w')
        slice_file.writelines(f'p{rsl}')
        slice_file.close()
        pfile = open(Part_label, 'w')
        if self.bios_type == "UEFI" and efi_exist is False:
            pfile.writelines('UEFI %s none\n' % bs)
        elif self.bios_type == "BIOS":
            pfile.writelines('BOOT %s none\n' % bs)
        pfile.writelines(f'{fs} {rootNum} {layout}\n')
        pfile.writelines('SWAP %s none\n' % int(swap - 1))
        pfile.close()
        pl = []
        mpl = []
        if self.bios_type == "UEFI" and efi_exist is False:
            if not os.path.exists(tmp + 'create'):
                pl.extend(([disk + "p%s" % sl, bs]))
                mpl.append(pl)
                cf = open(tmp + 'create', 'wb')
                pickle.dump(mpl, cf)
                cf.close()
        elif self.bios_type == "BOOT":
            pl.extend(([disk + "p%s" % sl, bs]))
            mpl.append(pl)
            cf = open(tmp + 'create', 'wb')
            pickle.dump(mpl, cf)
            cf.close()


class createLabel():
    def __init__(self, path, disk, partition_behind, left_size, create_size, label, fs, data):
        if not os.path.exists(disk_file):
            file_disk = open(disk_file, 'w')
            file_disk.writelines('%s\n' % disk)
            file_disk.close()
        sl = path[1] + 1
        lv = path[2]
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=MBR')
        sfile.close()
        slice_file = open(dslice, 'w')
        slice_file.writelines('s%s\n' % sl)
        slice_file.close()
        alph = ord('a')
        alph += lv
        letter = chr(alph)
        llist = []
        mllist = label_query(disk + 's%s' % sl)
        plf = open(partitiondb + disk + 's%s' % sl, 'wb')
        if left_size == 0:
            create_size -= 1
        if fs == "ZFS":
            label = "/(compress=lz4|atime=off),/root(compress=lz4)," \
                "/tmp(compress=lz4),/usr(canmount=off|mountpoint=none)," \
                "/usr/home(compress=lz4),/usr/jails(compress=lz4)," \
                "/usr/obj(compress=lz4),/usr/ports(compress=lz4)," \
                "/usr/src(compress=lz4)," \
                "/var(canmount=off|atime=on|mountpoint=none)," \
                "/var/audit(compress=lz4),/var/log(compress=lz4)," \
                "/var/mail(compress=lz4),/var/tmp(compress=lz4)"
        llist.extend(([disk + 's%s' % sl + letter, create_size, label, fs]))
        mllist[lv] = llist
        llist = []
        if left_size > 0:
            llist.extend((['freespace', left_size, '', '']))
            mllist.insert(lv + 1, llist)
        pickle.dump(mllist, plf)
        plf.close()
        llist = open(partitiondb + disk + 's%s' % sl, 'rb')
        labellist = pickle.load(llist)
        pfile = open(Part_label, 'w')
        for partlist in labellist:
            if partlist[2] != '':
                pfile.writelines('%s %s %s\n' % (partlist[3], partlist[1],
                                                 partlist[2]))
        pfile.close()


class modifyLabel():

    def __init__(self, path, left_size, create_size, label, fs, data, disk):
        if not os.path.exists(disk_file):
            file_disk = open(disk_file, 'w')
            file_disk.writelines('%s\n' % disk)
            file_disk.close()
        sl = path[1] + 1
        lv = path[2]
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=MBR')
        sfile.close()
        slice_file = open(dslice, 'w')
        slice_file.writelines('s%s\n' % sl)
        slice_file.close()
        alph = ord('a')
        alph += lv
        letter = chr(alph)
        llist = []
        mllist = label_query(disk + 's%s' % sl)
        plf = open(partitiondb + disk + 's%s' % sl, 'wb')
        if left_size == 0:
            create_size -= 1
        llist.extend(([disk + 's%s' % sl + letter, create_size, label, fs]))
        mllist[lv] = llist
        llist = []
        if left_size > 0:
            llist.extend((['freespace', left_size, '', '']))
            mllist.append(llist)
        pickle.dump(mllist, plf)
        plf.close()
        llist = open(partitiondb + disk + 's%s' % sl, 'rb')
        labellist = pickle.load(llist)
        pfile = open(Part_label, 'w')
        for partlist in labellist:
            if partlist[2] != '':
                pfile.writelines('%s %s %s\n' % (partlist[3], partlist[1],
                                                 partlist[2]))
        pfile.close()


class createSlice():

    def __init__(self, size, rs, path, disk):
        file_disk = open(disk_file, 'w')
        file_disk.writelines('%s\n' % disk)
        file_disk.close()
        if len(path) == 1:
            sl = 1
        else:
            sl = path[1] + 1
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=MBR')
        sfile.close()
        slice_file = open(dslice, 'w')
        slice_file.writelines('s%s\n' % sl)
        slice_file.close()
        plist = partition_query(disk)
        pslice = '%ss%s' % (disk, path[1] + 1)
        if rs == 0:
            size -= 1
        plist[path[1]] = [pslice, size, '', 'freebsd']
        if rs > 0:
            plist.append(['freespace', rs, '', ''])
        psf = open(partitiondb + disk, 'wb')
        pickle.dump(plist, psf)
        psf.close()
        llist = []
        mllist = []
        llist.extend((['freespace', size, '', '']))
        mllist.append(llist)
        plf = open(partitiondb + pslice, 'wb')
        pickle.dump(mllist, plf)
        plf.close()
        slice_file = open(dslice, 'w')
        slice_file.writelines('s%s\n' % pslice)
        slice_file.close()
        pl = []
        mpl = []
        if os.path.exists(tmp + 'create'):
            pf = open(tmp + 'create', 'rb')
            mpl = pickle.load(pf)
        pl.extend(([pslice, size]))
        mpl.append(pl)
        cf = open(tmp + 'create', 'wb')
        pickle.dump(mpl, cf)
        cf.close()


class createPartition():
    def __init__(self, path, disk, partition_behind, left_size, create_size, label, fs, create):
        if not os.path.exists(disk_file):
            file_disk = open(disk_file, 'w')
            file_disk.writelines('%s\n' % disk)
            file_disk.close()
        if partition_behind is None:
            pl = 1
            lv = 0
        else:
            p_behind = int(partition_behind.partition('p')[2])
            pl = p_behind + 1
            lv = path[1]
        if not os.path.exists(part_schem):
            sfile = open(part_schem, 'w')
            sfile.writelines('partscheme=GPT')
            sfile.close()
        if label == '/' or fs == "ZFS" or fs == "UEFI" or fs == "BOOT":
            slice_file = open(dslice, 'w')
            slice_file.writelines('p%s\n' % pl)
            # slice_file.writelines('%s\n' % number)
            slice_file.close()
        plist = []
        pslice = '%sp%s' % (disk, pl)
        mplist = partition_query(disk)
        if left_size == 0 and create_size > 1:
            create_size -= 1
        if fs == "ZFS":
            label = "/(compress=lz4|atime=off),/root(compress=lz4)," \
                "/tmp(compress=lz4),/usr(canmount=off|mountpoint=none)," \
                "/usr/home(compress=lz4),/usr/jails(compress=lz4)," \
                "/usr/obj(compress=lz4),/usr/ports(compress=lz4)," \
                "/usr/src(compress=lz4)," \
                "/var(canmount=off|atime=on|mountpoint=none)," \
                "/var/audit(compress=lz4),/var/log(compress=lz4)," \
                "/var/mail(compress=lz4),/var/tmp(compress=lz4)"
        pf = open(partitiondb + disk, 'wb')
        plist.extend(([disk + 'p%s' % pl, create_size, label, fs]))
        mplist[lv] = plist
        plist = []
        if left_size > 0:
            plist.extend((['freespace', left_size, '', '']))
            mplist.insert(lv + 1, plist)
        pickle.dump(mplist, pf)
        pf.close()
        pfile = open(Part_label, 'w')
        for partlist in partition_query(disk):
            if partlist[2] != '':
                pfile.writelines('%s %s %s\n' % (partlist[3], partlist[1],
                                                 partlist[2]))
        pfile.close()
        if create is True:
            plst = []
            mplst = []
            if not os.path.exists(tmp + 'create'):
                plst.extend(([pslice, create_size]))
                mplst.append(plst)
                cf = open(tmp + 'create', 'wb')
                pickle.dump(mplst, cf)
                cf.close()


class modifyPartition():

    def __init__(self, path, left_size, inumb, create_size, label, fs, data, disk):
        if not os.path.exists(disk_file):
            file_disk = open(disk_file, 'w')
            file_disk.writelines('%s\n' % disk)
            file_disk.close()
        if len(path) == 1:
            pl = 1
            lv = 0
        else:
            pl = path[1] + 1
            lv = path[1]
        if not os.path.exists(part_schem):
            sfile = open(part_schem, 'w')
            sfile.writelines('partscheme=GPT')
            sfile.close()
        if label == '/':
            slice_file = open(dslice, 'w')
            slice_file.writelines('p%s\n' % pl)
            slice_file.close()
        plist = []
        pslice = '%sp%s' % (disk, pl)
        mplist = partition_query(disk)
        if left_size == 0:
            create_size -= 1
        pf = open(partitiondb + disk, 'wb')
        plist.extend(([disk + 'p%s' % pl, create_size, label, fs]))
        mplist[lv] = plist
        plist = []
        if left_size > 0:
            plist.extend((['freespace', left_size, '', '']))
            mplist.append(plist)
        pickle.dump(mplist, pf)
        pf.close()
        pfile = open(Part_label, 'w')
        for partlist in partition_query(disk):
            if partlist[2] != '':
                pfile.writelines('%s %s %s\n' % (partlist[3], partlist[1],
                                 partlist[2]))
        pfile.close()
        if data is True:
            plst = []
            mplst = []
            if not os.path.exists(tmp + 'create'):
                plst.extend(([pslice, create_size]))
                mplst.append(plst)
                cf = open(tmp + 'create', 'wb')
                pickle.dump(mplst, cf)
                cf.close()


class rDeleteParttion():
    def __init__(self):
        if os.path.exists(tmp + 'delete'):
            delete_file = open(tmp + 'delete', 'rb')
            delete_list = pickle.load(delete_file)
            for partition in delete_list:
                num = slice_number(partition)
                drive = get_disk_from_partition(partition)
                call(f"zpool labelclear -f {partition}", shell=True)
                sleep(1)
                call(f'gpart delete -i {num} {drive}', shell=True)
                sleep(1)


class destroyParttion():
    def __init__(self):
        if os.path.exists(tmp + 'destroy'):
            dsf = open(tmp + 'destroy', 'rb')
            ds = pickle.load(dsf)
            for line in ds:
                drive = line[0]
                scheme = line[1]
                # Destroy the disk geom
                gpart_destroy = f"gpart destroy -F {drive}"
                call(gpart_destroy, shell=True)
                sleep(1)
                # Make double-sure
                create_gpt = f"gpart create -s gpt {drive}"
                call(create_gpt, shell=True)
                sleep(1)
                call(gpart_destroy, shell=True)
                sleep(1)
                clear_drive = f"dd if=/dev/zero of={drive} bs=1m count=1"
                call(clear_drive, shell=True)
                sleep(1)
                call(f'gpart create -s {scheme} {drive}', shell=True)
                sleep(1)


def bios_or_uefi():
    cmd = "sysctl -n machdep.bootmethod"
    output1 = Popen(cmd, shell=True, stdout=PIPE,
                    universal_newlines=True, close_fds=True)
    return output1.stdout.readlines()[0].rstrip()


class makingParttion():

    def __init__(self):
        if os.path.exists(tmp + 'create'):
            pf = open(tmp + 'create', 'rb')
            pl = pickle.load(pf)
            read = open(boot_file, 'r')
            boot = read.readlines()[0].strip()
            size = 0
            for line in pl:
                part = line[0]
                drive = get_disk_from_partition(part)
                sl = slice_number(part)
                size = int(line[1])
                if set("p") & set(part):
                    if bios_or_uefi() == 'UEFI':
                        cmd = f'gpart add -a 4k -s {size}M -t efi -i {sl} {drive}'
                        sleep(2)
                        cmd2 = f'newfs_msdos -F 16 {drive}p{sl}'
                        call(cmd, shell=True)
                        call(cmd2, shell=True)
                    else:
                        if boot == "grub":
                            cmd = f'gpart add -a 4k -s {size}M -t bios-boot -i {sl} {drive}'
                        else:
                            cmd = f'gpart add -a 4k -s {size}M -t freebsd-boot -i {sl} {drive}'
                        call(cmd, shell=True)
                elif set("s") & set(part):
                    cmd = f'gpart add -a 4k -s {size}M -t freebsd -i {sl} {drive}'
                    call(cmd, shell=True)
                sleep(2)
