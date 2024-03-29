# _*_ coding: utf-8 _*_

import sys
import json
import re
import codecs
import csv
from rdflib import Namespace, URIRef, Graph, BNode, Literal
from rdflib.namespace import RDF, RDFS, FOAF

csv.field_size_limit(1000000000)


# make rdf file
def make_rdf(infile_pubtator, outfile_rdf):
    g = Graph()

    data        = Namespace("http://www.w3.org/ns/oa#")
    ns_oa       = Namespace("http://www.w3.org/ns/oa#")
    ns_dcterms  = Namespace("http://purl.org/dc/terms/")
    ns_pubmed   = Namespace("http://rdf.ncbi.nlm.nih.gov/pubmed/")
    ns_dbsnp    = Namespace("http://identifiers.org/dbsnp/")
    ns_ncbigene = Namespace("http://identifiers.org/ncbigene/")
    ns_mesh     = Namespace("http://id.nlm.nih.gov/mesh/")
    ns_omim     = Namespace("http://identifiers.org/omim/")
    
    g.bind('oa', ns_oa)
    g.bind('dcterms', ns_dcterms)
    g.bind('pubmed', ns_pubmed)
    g.bind('dbsnp', ns_dbsnp)
    g.bind('ncbigene', ns_ncbigene)
    g.bind('mesh', ns_mesh)
    g.bind('omim', ns_omim)


    fh_in = open(infile_pubtator, 'r')
    #reader = csv.reader(fh_in, delimiter="\t")
    lines = fh_in.readlines()
    row_num = 0
    for line in lines:
        row = line.rstrip('\n').split('\t')
        pmid      = row[0]
        component = row[2]
        # skip non rs number
        match = re.match(u'^rs', component)
        if not match:
            continue

        mention   = row[3]
        resource    = row[4]
        list_resource = resource.split('|')

        # skip header
        if pmid == "PMID":
            continue

        blank = BNode()

        g.add( (blank, RDF.type, URIRef(ns_oa.Annotation)) )
        g.add( (blank, URIRef(ns_oa.hasTarget), URIRef(ns_pubmed + pmid)) )
        component = component.replace(' ', '')
        component = component.split(';')[0]
        g.add( (blank, URIRef(ns_oa.hasBody), URIRef(ns_dbsnp + component)) )
        for s in list_resource:
            g.add( (blank, URIRef(ns_dcterms.source), Literal(s)) )
    
    # output RDF
    g.serialize(destination=outfile_rdf, format='turtle')

    fh_in.close()
    return


# main
if __name__ == "__main__":
    params = sys.argv
    infile_pubtator  = params[1]
    outfile_rdf      = params[2]
    make_rdf(infile_pubtator, outfile_rdf)
