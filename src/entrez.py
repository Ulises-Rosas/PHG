import re
import urllib.request

class entrez:

    def __init__(self,
                 term="",
                 type="",
                 db="",
                 gene_string="",
                 Lmin="",
                 Lmax="",
                 cache = 200,
                 printing = True):

        self.type = type
        self.term = term.replace(" ", "%20") 
        self.db = db
        self.cache = cache
        self.printing = printing

        termType = "[Organism]" if not re.findall("\[", self.term) else ""

        if self.db == "nuccore":

            if gene_string != "" and len(gene_string.split(",")) == 1:
                gene_string = " OR ".join([i + "[All Fields]" for i in gene_string.split(",")])

            elif gene_string != "" and len(gene_string.split(",")) > 1:
                gene_string = "(" + \
                       " OR ".join([i + "[All Fields]" for i in gene_string.split(",")]) + \
                       ")"

            if Lmin != "" and Lmax != "":
                Lrange = "(" + str(Lmin) + "[SLEN] :" + str(Lmax) + "[SLEN])"
            else:
                Lrange = ""

            self.term = re.sub(" ",
                               "%20",
                               " AND ".join(
                                   [i for i in [self.term + termType, gene_string, Lrange] if i != ""]
                                    )
                               )

        self.esarch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=" + \
                          self.db + "&term=" + self.term

        self.efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=" + self.db

        self.ids = []

    def _get_ids(self):

        page = None

        while page is None:
            try:
                page = urllib.request.urlopen(self.esarch_url).read().decode('utf-8')

            except urllib.error.HTTPError:
                pass

        counts = re.sub(".*><Count>([0-9]+)</Count><.*", "\\1", page.replace("\n", ""))

        complete_esearch_url = self.esarch_url + "&retmax=" + counts

        ids_page = urllib.request.urlopen(complete_esearch_url).read().decode('utf-8')

        self.ids = [re.sub("<Id>([0-9\.]+)</Id>", "\\1", i) for i in re.findall("<Id>[0-9\.]+</Id>", ids_page)]

        return self.ids

    def _get_type(self, type = None):

        if type is not None:
            self.type = type

        ids = self._get_ids() if not self.ids else self.ids

        if not ids:
            return None
            
        out = ""
        i   = 0

        while i <= len(ids):

            target_url = self.efetch_url + \
                         "&id=" + ",".join( ids[i:i + self.cache] ) + \
                         "&rettype=" + self.type
    
            tmp_out    = urllib.request.urlopen(target_url).read().decode('utf-8')

            out += tmp_out
            i   += self.cache

        return out
