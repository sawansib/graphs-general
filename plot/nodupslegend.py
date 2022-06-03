import pychart.theme

class T(pychart.legend.T):
    def draw(self, ar, entries, can):

        entries_without_dups = []
        for i in entries:
            curr = [e.label for e in entries_without_dups]
            if i.label not in curr:
                entries_without_dups.append(i)
        entries = entries_without_dups

        pychart.legend.T.draw(self, ar, entries, can)
        
