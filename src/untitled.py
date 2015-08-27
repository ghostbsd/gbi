

def find_if_lable(seff, part):
        last = part[-1]
        if re.search('[a-z]', last):
            return True

    def __init__(self, part, path):
        if part == "freespace":
            pass
        elif self.find_if_lable(part) is True:
            spart = part[:-1]
            self.delete_label(part, spart, path)
        else:
            drive = rpartslice(part)
            self.delete_slice(drive, part, path)

    def modify_label(self, part, spart, path):
        llist = open(partitiondb + spart, 'r')
        ll = pickle.load(llist)
        last_num = len(ll) - 1
        lnum = path[2]
        # See if partlable exist to delete partiton
        if os.path.exists(Part_label):
            p_file = open(Part_label, 'r')
            pf = p_file.readlines()
            pnum = len(pf)
            # Look if or more item.
            if pnum == 1:
                os.remove(Part_label)
            else:
                pfile = open(Part_label, 'w')
                pf.pop(lnum)
                for line in pf:
                    pfile.writelines('%s' % line)
                pfile.close()
        if last_num == lnum:
            free = int_size(ll[last_num][1])
            if lnum != 0 and ll[lnum - 1][0] == 'freespace':
                free = free + int_size(ll[lnum - 1][1])
                ll[lnum] = ['freespace', free, '', '']
                ll.remove(ll[lnum - 1])
            else:
                ll[lnum] = ['freespace', free, '', '']
        elif lnum == 0:
            free = int_size(ll[lnum][1])
            if ll[lnum + 1][0] == 'freespace':
                free = free + int_size(ll[lnum + 1][1])
                ll.remove(ll[lnum + 1])
            ll[lnum] = ['freespace', free, '', '']
        else:
            free = int_size(ll[lnum][1])
            if ll[lnum + 1][0] == 'freespace':
                free = free + int_size(ll[lnum + 1][1])
                ll.remove(ll[lnum + 1])
            if lnum != 0 and ll[lnum - 1][0] == 'freespace':
                free = free + int_size(ll[lnum - 1][1])
                ll[lnum] = ['freespace', free, '', '']
                ll.remove(ll[lnum - 1])
            else:
                ll[lnum] = ['freespace', free, '', '']
        savepl = open(partitiondb + spart, 'w')
        pickle.dump(ll, savepl)
        savepl.close()

    def modify_partitonlabel(self, drive, part, path):
        slist = open(partitiondb + drive, 'rb')
        sl = pickle.load(slist)
        last_num = len(sl) - 1
        snum = path[1]
        if os.path.exists(dslice):
            sfile = open(dslice, 'r')
            slf = sfile.readlines()[0].rstrip()
            slnum = int(re.sub("[^0-9]", "", slf))
            ptnum = snum - slnum
        if os.path.exists(Part_label):
            p_file = open(Part_label, 'r')
            pf = p_file.readlines()
            pnum = len(pf)
            # Look if one or more item.
            if 's' in part:
                os.remove(Part_label)
            elif pnum == 1:
                os.remove(Part_label)
            else:
                pfile = open(Part_label, 'w')
                pf.pop(ptnum)
                for line in pf:
                    pfile.writelines('%s' % line)
                pfile.close()
        if last_num == snum:
            free = int_size(sl[last_num][1])
            if free == 1:
                sl.remove(sl[snum])
            else:
                if snum != 0 and sl[snum - 1][0] == 'freespace':
                    free = free + int_size(sl[snum - 1][1])
                    sl[snum] = ['freespace', free, '', '']
                    sl.remove(sl[snum - 1])
                else:
                    sl[snum] = ['freespace', free, '', '']
        elif snum == 0:
            free = int_size(sl[snum][1])
            if free == 1:
                sl.remove(sl[snum])
            else:
                if sl[snum + 1][0] == 'freespace':
                    free = free + int_size(sl[snum + 1][1])
                    sl.remove(sl[snum + 1])
                    sl[snum] = ['freespace', free, '', '']
        else:
            free = int_size(sl[snum][1])
            if sl[snum + 1][0] == 'freespace' and sl[snum - 1][0] == 'freespace':
                if free == 1:
                    free = int_size(sl[snum + 1][1]) + int_size(sl[snum - 1][1])
                    sl[snum] = ['freespace', free, '', '']
                    sl.remove(sl[snum + 1])
                    sl.remove(sl[snum - 1])
                else:
                    free = free + int_size(sl[snum + 1][1]) + int_size(sl[snum - 1][1])
                    sl[snum] = ['freespace', free, '', '']
                    sl.remove(sl[snum + 1])
                    sl.remove(sl[snum - 1])
            elif sl[snum + 1][0] == 'freespace':
                if free == 1:
                    sl.remove(sl[snum])
                else:
                    free = free + int_size(sl[snum + 1][1])
                    sl[snum] = ['freespace', free, '', '']
                    sl.remove(sl[snum + 1])
            elif snum != 0 and sl[snum - 1][0] == 'freespace':
                if free == 1:
                    sl.remove(sl[snum])
                else:
                    free = free + int_size(sl[snum - 1][1])
                    sl[snum] = ['freespace', free, '', '']
                    sl.remove(sl[snum - 1])
            else:
                sl[snum] = ['freespace', free, '', '']
        # Making delete file
        dl = []
        mdl = []
        data = True
        # if delete exist chek if slice is in delete.
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
        saveps = open(partitiondb + drive, 'w')
        pickle.dump(sl, saveps)
        saveps.close()