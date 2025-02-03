import csv
import xml.etree.ElementTree as ET
import lxml.etree as etree

def create_camt053(csv_file, xml_file):
    # Read CSV file
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # Create the root element
        root = ET.Element('Document')
        root.set('xmlns', 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.02')

        # Create the BkToCstmrStmt element
        bk_to_cstmr_stmt = ET.SubElement(root, 'BkToCstmrStmt')

        # Create the Stmt element
        stmt = ET.SubElement(bk_to_cstmr_stmt, 'Stmt')

        # Add some static elements
        ET.SubElement(stmt, 'Id').text = 'STATEMENT_ID'
        ET.SubElement(stmt, 'CreDtTm').text = '2025-01-31T00:00:00'
        TotalAmt = 0.0

        # Create the Ntry elements from CSV rows
        for row in reader:
            ntry = ET.SubElement(stmt, 'Ntry')
            ET.SubElement(ntry, 'Amt').text = row['Bedrag (EUR)']
            TotalAmt += float(row['Bedrag (EUR)'].replace(",", ".")) if row['Af Bij'] == 'Bij' else -float(row['Bedrag (EUR)'].replace(",", "."))
            ET.SubElement(ntry, 'CdtDbtInd').text = 'DBIT' if row['Af Bij'] == 'Af' else 'CRDT'
            ET.SubElement(ntry, 'BookgDt').text = row['Datum']
            ET.SubElement(ntry, 'ValDt').text = row['Datum']
            tx_dtls = ET.SubElement(ntry, 'NtryDtls')
            tx_dtls = ET.SubElement(tx_dtls, 'TxDtls')
            refs = ET.SubElement(tx_dtls, 'Refs')
            ET.SubElement(refs, 'EndToEndId').text = row['Mededelingen']
            rltd_pties = ET.SubElement(tx_dtls, 'RltdPties')
            dbtr = ET.SubElement(rltd_pties, 'Dbtr')
            ET.SubElement(dbtr, 'Nm').text = row['Naam / Omschrijving']
            dbtr_acct = ET.SubElement(rltd_pties, 'DbtrAcct')
            ET.SubElement(dbtr_acct, 'Id').text = row['Rekening']
            cdtr = ET.SubElement(rltd_pties, 'Cdtr')
            ET.SubElement(cdtr, 'Nm').text = row['Tegenrekening']

        # Write the XML to a file
        tree = ET.ElementTree(root)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)
        x = etree.parse(xml_file)
        print(etree.tostring(x, pretty_print=True).decode())
        print('TotalAmt:', round(TotalAmt, 2))

# Usage specify input and output file
csv_file = 'inputfile.csv'
xml_file = 'output_camt053.xml'
create_camt053(csv_file, xml_file)
