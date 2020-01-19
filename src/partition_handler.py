#!/usr/bin/env python3

import os
import re
from subprocess import Popen, PIPE, STDOUT, call
import pickle
from time import sleep

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


def disk_query():
    df = open(diskdb, 'rb')
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


def how_partition(path):
    disk = disk_query()[path[0]][0]
    if os.path.exists(partitiondb + disk):
        part = partition_query(disk)
        return len(part)
    else:
        return 0


def first_is_free(path):
    disk = disk_query()[path[0]][0]
    if os.path.exists(partitiondb + disk):
        part = partition_query(disk)
        return part[0][0]
    else:
        return None


def partition_query(disk):
    plist = open(partitiondb + disk, 'rb')
    pl = pickle.load(plist)
    return pl


def label_query(pslice):
    llist = open(partitiondb + pslice, 'rb')
    ll = pickle.load(llist)
    return ll


def scheme_query(path):
    disk = disk_query()[path[0]]
    return disk[-1]


def find_scheme(disk):
    cmd = "%s %s" % (detect_sheme, disk)
    shm_out = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
                    universal_newlines=True, close_fds=True)
    scheme = shm_out.stdout.readlines()[0].rstrip()
    return scheme


def rpartslice(part):
    item = part
    p = set("p")
    s = set("s")
    if p & set(item):
        drive = item.partition('p')[0]
    elif s & set(item):
        drive = item.partition('s')[0]
    return drive


def sliceNum(part):
    item = part
    p = set("p")
    s = set("s")
    if p & set(item):
        num = int(item.partition('p')[2])
    elif s & set(item):
        num = int(item.partition('s')[2])
    return num


def slicePartition(part):
    item = part
    p = set("p")
    s = set("s")
    if p & set(item):
        return 'p'
    elif s & set(item):
        return 's'


class diskSchemeChanger():

    def __init__(self, schm, path, disk, size):
        dlist = disk_query()
        dselected = dlist[path[0]]
        if schm is None:
            dselected[-1] = 'GPT'
        else:
            dselected[-1] = schm
        dlist[path[0]] = dselected
        disk = dselected[0]
        df = open(diskdb, 'wb')
        pickle.dump(dlist, df)
        df.close()
        dsl = []
        mdsl = []
        if os.path.exists(tmp + 'destroy'):
            df = open(tmp + 'destroy', 'rb')
            mdsl = pickle.load(df)
        dsl.extend(([disk, schm]))
        mdsl.append(dsl)
        cf = open(tmp + 'destroy', 'wb')
        pickle.dump(mdsl, cf)
        cf.close()
        if not os.path.exists(partitiondb + disk):
            plist = []
            mplist = []
            psf = open(partitiondb + disk, 'wb')
            plist.extend((['freespace', size, '', '']))
            mplist.append(plist)
            pickle.dump(mplist, psf)
            psf.close()


class partition_repos():

    def disk_list(self):
        disk_output = Popen(query_disk, shell=True, stdin=PIPE, stdout=PIPE,
                            universal_newlines=True,  close_fds=True)
        dlist = []
        for disk in disk_output.stdout:
            dlist.append(disk.split())
        return dlist

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

    def mbr_partition_slice_list(self, disk):
        partition_outpput = Popen('%s %s' % (query_partition, disk),
                                  shell=True, stdin=PIPE, stdout=PIPE,
                                  universal_newlines=True, close_fds=True)
        plist = []
        mplist = []
        dpsf = open(partitiondb + disk, 'wb')
        for line in partition_outpput.stdout:
            info = line.split()
            plist.extend((info[0], info[1].partition('M')[0], '', info[2]))
            mplist.append(plist)
            plist = []
            self.mbr_partition_list(info[0])
        pickle.dump(mplist, dpsf)
        dpsf.close()

    def mbr_partition_list(self, pslice):
        slice_outpput = Popen('%s %s' % (query_label, pslice), shell=True,
                              stdin=PIPE, stdout=PIPE,
                              universal_newlines=True, close_fds=True)
        alph = ord('a')
        if pslice == 'freespace':
            pass
        else:
            llist = []
            mllist = []
            plf = open(partitiondb + pslice, 'wb')
            for line in slice_outpput.stdout:
                info = line.split()
                letter = chr(alph)
                alph = alph + 1
                if info[0] == 'freespace':
                    llist.extend(([info[0], info[1].partition('M')[0], '', ''])
                                 )
                else:
                    llist.extend((
                                 [pslice + letter, info[0].partition('M')[0],
                                  '', info[1]]))
                mllist.append(llist)
                llist = []
            pickle.dump(mllist, plf)
            plf.close()

    def gpt_partition_list(self, disk):
        partition_outpput = Popen('%s %s' % (query_partition, disk),
                                  shell=True, stdin=PIPE, stdout=PIPE,
                                  universal_newlines=True, close_fds=True)
        plist = []
        mplist = []
        psf = open(partitiondb + disk, 'wb')
        for line in partition_outpput.stdout:
            info = line.split()
            plist.extend((info[0], info[1].partition('M')[0], '', info[2]))
            mplist.append(plist)
            plist = []
        pickle.dump(mplist, psf)
        psf.close()

    def __init__(self):
        if not os.path.exists(partitiondb):
            os.makedirs(partitiondb)
        df = open(diskdb, 'wb')
        dlist = []
        mdlist = []
        for disk in self.disk_list():
            if self.find_Scheme(disk[0]) == "GPT":
                dlist.extend(([disk[0], self.disk_size(disk[0]), '', 'GPT']))
                self.gpt_partition_list(disk[0])
                mdlist.append(dlist)
            elif self.find_Scheme(disk[0]) == "MBR":
                dlist.extend(([disk[0], self.disk_size(disk[0]), '', 'MBR']))
                self.mbr_partition_slice_list(disk[0])
                mdlist.append(dlist)
            else:
                dlist.extend(([disk[0], self.disk_size(disk[0]), '', None]))
                mdlist.append(dlist)
            dlist = []
        pickle.dump(mdlist, df)
        df.close()


class Delete_partition():

    def find_if_lable(seff, part):
        last = part[-1]
        if re.search('[a-z]', last):
            return True

    def delete_label(self, part, spart, path):
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
        elif self.find_if_lable(part) is True:
            spart = part[:-1]
            self.delete_label(part, spart, path)
        else:
            drive = rpartslice(part)
            self.delete_slice(drive, part, path)

    def delete_slice(self, drive, part, path):
        slist = open(partitiondb + drive, 'rb')
        sl = pickle.load(slist)
        last_num = len(sl) - 1
        snum = path[1]
        if os.path.exists(dslice):
            sfile = open(dslice, 'r')
            slf = sfile.readlines()[0].rstrip()
            if slf == 'all':
                ptnum = snum - 1
            else:
                slnum = int(re.sub("[^0-9]", "", slf))
        if last_num == snum:
            free = int(sl[last_num][1])
            if snum != 0 and sl[snum - 1][0] == 'freespace':
                free = free + int(sl[snum - 1][1])
                sl[snum] = ['freespace', free, '', '']
                sl.remove(sl[snum - 1])
            else:
                sl[snum] = ['freespace', free, '', '']
        elif snum == 0:
            free = int(sl[snum][1])
            if sl[snum + 1][0] == 'freespace':
                free = free + int(sl[snum + 1][1])
                sl.remove(sl[snum + 1])
                sl[snum] = ['freespace', free, '', '']
            else:
                sl[snum] = ['freespace', free, '', '']
        else:
            free = int(sl[snum][1])
            slice_after = sl[snum + 1][0]
            slice_before = sl[snum - 1][0]
            size_after = sl[snum + 1][1]
            size_before = sl[snum - 1][1]
            if slice_after == 'freespace' and slice_before == 'freespace':
                free = free + int(size_after) + int(size_before)
                sl[snum] = ['freespace', free, '', '']
                sl.remove(sl[snum + 1])
                sl.remove(sl[snum - 1])
            elif slice_after == 'freespace':
                free = free + int(sl[snum + 1][1])
                sl[snum] = ['freespace', free, '', '']
                sl.remove(sl[snum + 1])
            elif snum != 0 and sl[snum - 1][0] == 'freespace':
                free = free + int(sl[snum - 1][1])
                sl[snum] = ['freespace', free, '', '']
                sl.remove(sl[snum - 1])
            else:
                sl[snum] = ['freespace', free, '', '']
        # Making delete file
        dl = []
        mdl = []
        data = True
        # if delete exist check if slice is in delete.
        if os.path.exists(tmp + 'delete'):
            df = open(tmp + 'delete', 'rb')
            mdl = pickle.load(df)
            for line in mdl:
                if part in line:
                    data = False
                    break
        if data is True:
            dl.extend(([part, free]))
            mdl.append(dl)
            cf = open(tmp + 'delete', 'wb')
            pickle.dump(mdl, cf)
            cf.close()
        if os.path.exists(partitiondb + part):
            os.remove(partitiondb + part)
        saveps = open(partitiondb + drive, 'wb')
        pickle.dump(sl, saveps)
        saveps.close()
        if "p" in part:
            pfile = open(Part_label, 'w')
            for partlist in partition_query(drive):
                if partlist[2] != '':
                    partition = f'{partlist[3]} {partlist[1]} {partlist[2]}\n'
                    pfile.writelines(partition)
            pfile.close()


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
        ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
                    universal_newlines=True, close_fds=True)
        mem = ram.stdout.read()
        swap = int(int(mem.partition(':')[2].strip()) / (1024 * 1024))
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

    def __init__(self, disk, size, schm):
        self.bios_type = bios_or_uefi()
        if schm == 'GPT':
            self.create_gpt_partiton(disk, size)
        elif schm == 'MBR':
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
        ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
                    universal_newlines=True,  close_fds=True)
        mem = ram.stdout.read()
        swap = int(int(mem.partition(':')[2].strip()) / (1024 * 1024))
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

    def create_mbr_partiton(self, disk, size, sl, path):
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
        ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
                    universal_newlines=True,  close_fds=True)
        mem = ram.stdout.read()
        swap = int(int(mem.partition(':')[2].strip()) / (1024 * 1024))
        rootNum = int(number - swap)
        llist = []
        mllist = []
        plf = open(partitiondb + disk + 's%s' % sl, 'wb')
        llist.extend(([disk + 's%sa' % sl, rootNum, '/', 'UFS+SUJ']))
        mllist.append(llist)
        llist = []
        llist.extend(([disk + 's%sb' % sl, swap, 'none', 'SWAP']))
        mllist.append(llist)
        pickle.dump(mllist, plf)
        plf.close()
        pfile = open(Part_label, 'w')
        pfile.writelines('UFS+SUJ %s /\n' % rootNum)
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

    def __init__(self, path, size, efi_exist=False):
        self.bios_type = bios_or_uefi()
        disk = disk_query()[path[0]][0]
        schm = disk_query()[path[0]][3]
        sl = path[1] + 1
        lv = path[1]
        if schm == "GPT":
            self.create_gpt_partiton(disk, size, sl, lv, efi_exist)
        elif schm == "MBR":
            self.create_mbr_partiton(disk, size, sl, lv)

    def create_gpt_partiton(self, disk, size, sl, path, efi_exist):
        file_disk = open(disk_file, 'w')
        file_disk.writelines('%s\n' % disk)
        file_disk.close()
        sfile = open(part_schem, 'w')
        sfile.writelines('partscheme=GPT')
        sfile.close()
        number = int(size.partition('M')[0])
        number = number - 512
        ram = Popen(memory, shell=True, stdin=PIPE, stdout=PIPE,
                    universal_newlines=True, close_fds=True)
        mem = ram.stdout.read()
        swap = int(int(mem.partition(':')[2].strip()) / (1024 * 1024))
        rootNum = int(number - swap)
        if bios_or_uefi() == "UEFI":
            bs = 256
        else:
            bs = 1
        rootNum = int(rootNum - bs)
        plist = []
        mplist = partition_query(disk)
        plf = open(partitiondb + disk, 'wb')
        done = False
        if self.bios_type == "UEFI" and efi_exist is False:
            plist.extend(([disk + 'p%s' % sl, bs, 'none', 'UEFI']))
            rsl = int(sl + 1)
            swsl = int(rsl + 1)
        elif self.bios_type == "UEFI" and efi_exist is True:
            rsl = int(sl)
            swsl = int(rsl + 1)
        else:
            plist.extend(([disk + 'p%s' % sl, bs, 'none', 'BOOT']))
            rsl = int(sl + 1)
            swsl = (rsl + 1)
        if len(plist) != 0:
            done = True
            mplist[path] = plist
            plist = []
        plist.extend(([disk + 'p%s' % rsl, rootNum, '/', 'UFS+SUJ']))
        if done is False:
            mplist[path] = plist
        else:
            mplist.append(plist)
        plist = []
        plist.extend(([disk + 'p%s' % swsl, swap, 'none', 'SWAP']))
        mplist.append(plist)
        pickle.dump(mplist, plf)
        plf.close()
        slice_file = open(dslice, 'w')
        slice_file.writelines(f'p{rsl}')
        slice_file.close()
        pfile = open(Part_label, 'w')
        if self.bios_type == "UEFI" and sl == 1:
            pfile.writelines('UEFI %s none\n' % bs)
        else:
            pfile.writelines('BOOT %s none\n' % bs)
        pfile.writelines('UFS+SUJ %s /\n' % rootNum)
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
        elif self.bios_type == "BOOT" and efi_exist is True:
            pass
        else:
            if not os.path.exists(tmp + 'create'):
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


class modifyLabel():

    def __init__(self, path, left_size, create_size, label, fs, data):
        disk = disk_query()[path[0]][0]
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

    def __init__(self, size, rs, path):
        disk = disk_query()[path[0]][0]
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
        if label == '/':
            slice_file = open(dslice, 'w')
            slice_file.writelines('p%s\n' % pl)
            # slice_file.writelines('%s\n' % number)
            slice_file.close()
        plist = []
        pslice = '%sp%s' % (disk, pl)
        mplist = partition_query(disk)
        if left_size == 0 and create_size > 1:
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

    def __init__(self, path, left_size, inumb, create_size, label, fs, data):
        disk = disk_query()[path[0]][0]
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
            df = open(tmp + 'delete', 'rb')
            dl = pickle.load(df)
            for line in dl:
                part = line[0]
                num = sliceNum(part)
                hd = rpartslice(part)
                call('gpart delete -i %s %s' % (num, hd), shell=True)
                sleep(2)


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
                zpool_clear = f"zpool labelclear -f ${drive}"
                call(gpart_destroy, shell=True)
                sleep(1)
                call(zpool_clear, shell=True)
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
    # cmd = "kenv grub.platform"
    # output = Popen(cmd, shell=True, stdout=PIPE,
    #                universal_newlines=True, close_fds=True)
    # kenvoutput = output.stdout.readlines()
    # if len(kenvoutput) == 0:
    #     cmd = "sysctl -n machdep.bootmethod"
    #     output1 = Popen(cmd, shell=True, stdout=PIPE,
    #                     universal_newlines=True, close_fds=True)
    #     return output1.stdout.readlines()[0].rstrip()
    # elif kenvoutput == "efi":
    #     return "UEFI"
    # else:
    #     return "BIOS"
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
                drive = rpartslice(part)
                sl = sliceNum(part)
                size = int(line[1])
                if slicePartition(part) == 'p':
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
                elif slicePartition(part) == 's':
                    cmd = f'gpart add -a 4k -s {size}M -t freebsd -i {sl} {drive}'
                    call(cmd, shell=True)
                sleep(2)
