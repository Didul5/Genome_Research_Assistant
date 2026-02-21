"""
genomic_db.py — Mock genomic knowledge base.

In a real system this would be backed by ClinVar, COSMIC, PubMed, etc.
For the prototype we hardcode ~30 curated entries that cover the
example queries well enough to demonstrate hybrid retrieval.
"""

GENOMIC_KNOWLEDGE_BASE = [
    # ── BRCA1 ──────────────────────────────────────────────
    {
        "id": "DOC-001",
        "title": "BRCA1 c.68_69delAG (185delAG) — Founder Mutation",
        "type": "variant_annotation",
        "gene": "BRCA1",
        "content": (
            "The BRCA1 c.68_69delAG mutation, historically known as 185delAG, "
            "is a frameshift deletion in exon 2 that introduces a premature stop codon "
            "at position 39. It is one of the three Ashkenazi Jewish founder mutations "
            "with an allele frequency of ~1% in that population. Carriers have a "
            "cumulative breast cancer risk of 60-80% by age 70 and an ovarian cancer "
            "risk of 20-40%. The truncated protein loses the RING domain and BRCT "
            "repeats, abolishing E3 ubiquitin ligase activity and DNA damage response "
            "signaling through the ATM/ATR pathway."
        ),
        "references": [
            "Struewing JP et al., N Engl J Med 1997;336:1401-1408",
            "King MC et al., Science 2003;302:643-646",
        ],
    },
    {
        "id": "DOC-002",
        "title": "BRCA1 in Homologous Recombination Repair",
        "type": "pathway",
        "gene": "BRCA1",
        "content": (
            "BRCA1 functions as a scaffold in the homologous recombination (HR) "
            "repair pathway. It forms the BRCA1-PALB2-BRCA2 complex that loads RAD51 "
            "onto resected DNA ends at double-strand breaks. Loss of BRCA1 shifts "
            "repair toward error-prone NHEJ, causing genomic instability. This is "
            "the mechanistic basis for PARP inhibitor sensitivity (synthetic lethality): "
            "PARP inhibition blocks single-strand break repair, forcing reliance on HR, "
            "which is defective in BRCA1-mutant cells."
        ),
        "references": [
            "Prakash R et al., Cold Spring Harb Perspect Biol 2015;7:a016600",
            "Lord CJ & Ashworth A, Science 2017;355:1152-1158",
        ],
    },
    {
        "id": "DOC-003",
        "title": "Clinical Management of BRCA1 Mutation Carriers",
        "type": "clinical",
        "gene": "BRCA1",
        "content": (
            "Current NCCN guidelines recommend enhanced screening for BRCA1 carriers: "
            "annual breast MRI starting at age 25, annual mammography starting at 30, "
            "and consideration of risk-reducing mastectomy and salpingo-oophorectomy "
            "by age 35-40. PARP inhibitors (olaparib, talazoparib) are approved for "
            "metastatic BRCA1-mutant breast cancer and platinum-sensitive ovarian cancer. "
            "Immunotherapy may benefit BRCA1-deficient tumors due to elevated tumor "
            "mutational burden and neoantigen load."
        ),
        "references": [
            "NCCN Guidelines v2.2024 — Genetic/Familial High-Risk Assessment",
            "Robson M et al., N Engl J Med 2017;377:523-533",
        ],
    },
    # ── TP53 ───────────────────────────────────────────────
    {
        "id": "DOC-004",
        "title": "TP53 Gene Structure and Function",
        "type": "gene_overview",
        "gene": "TP53",
        "content": (
            "TP53 encodes the p53 tumor suppressor protein, a transcription factor "
            "that responds to DNA damage, oncogene activation, and other stress signals. "
            "p53 activates cell cycle arrest (p21), apoptosis (BAX, PUMA, NOXA), and "
            "senescence programs. It is the most frequently mutated gene in human cancer, "
            "altered in >50% of all tumors. Most mutations cluster in the DNA-binding "
            "domain (exons 5-8), with hotspots at codons 175, 245, 248, 249, 273, and 282."
        ),
        "references": [
            "Kandoth C et al., Nature 2013;502:333-339",
            "Bouaoun L et al., Hum Mutat 2016;37:865-876",
        ],
    },
    {
        "id": "DOC-005",
        "title": "CRISPR-Based Approaches to TP53 Restoration",
        "type": "therapeutic_strategy",
        "gene": "TP53",
        "content": (
            "Several CRISPR strategies target TP53 in cancer research: (1) Base editing "
            "to correct hotspot missense mutations — ABE8e can revert R175H (c.524G>A) "
            "and R248W (c.742C>T) with high efficiency in organoid models. (2) CRISPRi "
            "to silence gain-of-function mutant TP53 alleles using allele-specific gRNAs "
            "that exploit SNPs in cis with the mutation. (3) CRISPR activation of p53 "
            "target genes (p21, MDM2 negative feedback) as an alternative to restoring "
            "p53 itself. Delivery remains the bottleneck — lipid nanoparticles and AAV "
            "vectors show promise in preclinical liver and lung tumor models."
        ),
        "references": [
            "Komor AC et al., Nature 2016;533:420-424",
            "Liu Y et al., Nat Biotechnol 2023;41:1023-1034",
        ],
    },
    {
        "id": "DOC-006",
        "title": "TP53 CRISPR Guide RNA Design Considerations",
        "type": "technical",
        "gene": "TP53",
        "content": (
            "Designing gRNAs for TP53 requires attention to: (1) Exonic targets in "
            "the DNA-binding domain (exons 5-8, chr17:7,577,498-7,578,811 on GRCh38). "
            "(2) PAM availability — SpCas9 (NGG) sites flanking codons 175, 248, 273. "
            "(3) Off-target filtering against the TP53 pseudogene TP53TG3 and processed "
            "pseudogenes on chr15. Tools: CRISPRscan, Benchling, CHOPCHOP. Recommended "
            "gRNA lengths: 19-20 nt with 40-60% GC content. For base editing, the edit "
            "window is positions 4-8 in the protospacer (counting PAM-distal as 1)."
        ),
        "references": [
            "Haeussler M et al., Genome Biol 2016;17:148",
            "Rees HA & Liu DR, Nat Rev Genet 2018;19:770-788",
        ],
    },
    # ── KRAS ───────────────────────────────────────────────
    {
        "id": "DOC-007",
        "title": "KRAS in Pancreatic Ductal Adenocarcinoma",
        "type": "gene_disease",
        "gene": "KRAS",
        "content": (
            "Oncogenic KRAS mutations are present in >90% of pancreatic ductal "
            "adenocarcinoma (PDAC). The most common variant is G12D (~40%), followed by "
            "G12V (~30%) and G12R (~15%). Mutant KRAS locks the GTPase in the GTP-bound "
            "active state, constitutively driving RAF-MEK-ERK and PI3K-AKT-mTOR "
            "signaling cascades. KRAS activation is considered the initiating event, "
            "with subsequent loss of CDKN2A, TP53, and SMAD4 driving progression "
            "through PanIN stages I-III to invasive carcinoma."
        ),
        "references": [
            "Bailey P et al., Nature 2016;531:47-52",
            "Waters AM & Der CJ, Cold Spring Harb Perspect Med 2018;8:a031435",
        ],
    },
    {
        "id": "DOC-008",
        "title": "KRAS G12C Inhibitors and Pancreatic Cancer",
        "type": "therapeutic",
        "gene": "KRAS",
        "content": (
            "Sotorasib (AMG 510) and adagrasib (MRTX849) covalently bind the switch-II "
            "pocket of KRAS G12C, trapping it in the inactive GDP-bound state. While "
            "approved for NSCLC, G12C is rare in PDAC (~1-2%). For the dominant G12D "
            "mutation, MRTX1133 is a first-in-class non-covalent inhibitor showing "
            "preclinical activity. Combination strategies under investigation include "
            "KRAS G12D inhibition + anti-PD1, SHP2 inhibitors, and CDK4/6 inhibitors "
            "to overcome adaptive resistance through ERK reactivation."
        ),
        "references": [
            "Hallin J et al., Cancer Discov 2022;12:1204-1217",
            "Kim D et al., Nature 2023;615:687-693",
        ],
    },
    {
        "id": "DOC-009",
        "title": "KRAS Signaling Pathway — RAS-RAF-MEK-ERK",
        "type": "pathway",
        "gene": "KRAS",
        "content": (
            "KRAS functions as a molecular switch in the RAS-RAF-MEK-ERK (MAPK) "
            "signaling cascade. Growth factor receptors (EGFR, HER2) activate SOS, "
            "a GEF that promotes GTP loading on KRAS. Active KRAS-GTP recruits RAF "
            "kinases (BRAF, CRAF) to the membrane, initiating a phosphorylation cascade "
            "through MEK1/2 and ERK1/2. ERK activates transcription factors (ETS, MYC) "
            "driving proliferation. GTPase-activating proteins (GAPs like NF1) normally "
            "terminate signaling by stimulating GTP hydrolysis, but oncogenic KRAS "
            "mutations impair GAP-mediated hydrolysis, leading to constitutive activation."
        ),
        "references": [
            "Downward J, Nat Rev Cancer 2003;3:11-22",
            "Simanshu DK et al., Cell 2017;170:209-223",
        ],
    },
    {
        "id": "DOC-010",
        "title": "Pancreatic Cancer Genomic Landscape",
        "type": "genomic_overview",
        "gene": "multi",
        "content": (
            "Whole-genome sequencing of PDAC reveals four subtypes: squamous, "
            "pancreatic progenitor, immunogenic, and aberrantly differentiated endocrine/"
            "exocrine (ADEX). The core driver mutations are KRAS (92%), TP53 (72%), "
            "CDKN2A (30%), and SMAD4 (32%). Structural variants are frequent, with "
            "chromothripsis in ~10% of cases. The tumor microenvironment is dense with "
            "cancer-associated fibroblasts and immunosuppressive myeloid cells, "
            "contributing to the poor response to immunotherapy. Median overall survival "
            "remains ~6-12 months for metastatic disease."
        ),
        "references": [
            "Waddell N et al., Nature 2015;518:495-501",
            "Cancer Genome Atlas Research Network, Cancer Cell 2017;32:185-203",
        ],
    },
    # ── EGFR ───────────────────────────────────────────────
    {
        "id": "DOC-011",
        "title": "EGFR Mutations in Non-Small Cell Lung Cancer",
        "type": "variant_annotation",
        "gene": "EGFR",
        "content": (
            "Activating EGFR mutations in NSCLC cluster in the tyrosine kinase domain "
            "(exons 18-21). The two most common are exon 19 deletions (~45%) and "
            "L858R point mutation in exon 21 (~40%). These mutations increase kinase "
            "activity and sensitivity to EGFR TKIs (gefitinib, erlotinib, osimertinib). "
            "The T790M gatekeeper mutation in exon 20 confers resistance to first/second-"
            "gen TKIs but is overcome by osimertinib (third-gen). Exon 20 insertions "
            "represent ~10% of EGFR mutations and are generally TKI-resistant."
        ),
        "references": [
            "Mok TS et al., N Engl J Med 2009;361:947-957",
            "Soria JC et al., N Engl J Med 2018;378:113-125",
        ],
    },
    # ── General genomics ───────────────────────────────────
    {
        "id": "DOC-012",
        "title": "DNA Damage Response and Repair Mechanisms",
        "type": "pathway",
        "gene": "multi",
        "content": (
            "The DNA damage response (DDR) encompasses several repair pathways: "
            "base excision repair (BER) for oxidative damage, nucleotide excision "
            "repair (NER) for bulky adducts, mismatch repair (MMR) for replication "
            "errors, homologous recombination (HR) and non-homologous end joining (NHEJ) "
            "for double-strand breaks. Sensor kinases ATM and ATR activate checkpoint "
            "signaling through CHK1/CHK2, leading to p53-dependent cell cycle arrest "
            "or apoptosis. DDR defects are exploited therapeutically via synthetic "
            "lethality (e.g., PARP inhibitors in HR-deficient tumors)."
        ),
        "references": [
            "Jackson SP & Bartek J, Nature 2009;461:1071-1078",
            "Lord CJ & Ashworth A, Nature 2012;481:287-294",
        ],
    },
    {
        "id": "DOC-013",
        "title": "Tumor Mutational Burden and Immunotherapy Response",
        "type": "biomarker",
        "gene": "multi",
        "content": (
            "Tumor mutational burden (TMB) — the number of somatic mutations per megabase "
            "— is a predictive biomarker for immune checkpoint inhibitor response. "
            "High TMB (≥10 mut/Mb, FDA threshold) correlates with increased neoantigen "
            "load, promoting T-cell recognition. TMB-high tumors include melanoma, NSCLC, "
            "and MSI-high colorectal cancer. Pembrolizumab has a tissue-agnostic approval "
            "for TMB-high solid tumors. However, TMB alone has limited predictive value "
            "in some cancer types (e.g., pancreatic, prostate) due to immunosuppressive "
            "microenvironment factors."
        ),
        "references": [
            "Marabelle A et al., Ann Oncol 2020;31:1084-1091",
            "Samstein RM et al., Nat Genet 2019;51:202-206",
        ],
    },
    {
        "id": "DOC-014",
        "title": "CRISPR-Cas9 Mechanism and Applications in Cancer",
        "type": "technology",
        "gene": "multi",
        "content": (
            "CRISPR-Cas9 uses a guide RNA (gRNA) to direct the Cas9 endonuclease to "
            "a specific genomic locus, creating a double-strand break 3 bp upstream of "
            "the PAM sequence (NGG for SpCas9). Repair by NHEJ introduces indels "
            "(knockouts), while HDR with a donor template enables precise edits. In "
            "cancer research, CRISPR is used for: functional genomic screens to identify "
            "dependencies, engineering CAR-T cells, correcting driver mutations in "
            "organoids, and creating accurate mouse models. Base editors (ABE, CBE) and "
            "prime editors extend precision without double-strand breaks."
        ),
        "references": [
            "Doudna JA & Charpentier E, Science 2014;346:1258096",
            "Stadtmauer EA et al., Science 2020;367:eaba7365",
        ],
    },
    {
        "id": "DOC-015",
        "title": "BRCA1 c.68_69delAG — Population Genetics",
        "type": "population_genetics",
        "gene": "BRCA1",
        "content": (
            "The 185delAG mutation originated approximately 2,000 years ago and spread "
            "through genetic drift and possible founder effects in the Ashkenazi Jewish "
            "population. Carrier frequency is approximately 1.1% (1 in 90). It also "
            "appears at lower frequencies in Iraqi Jewish and Hispanic populations, "
            "likely through shared Sephardic ancestry. Population-based screening "
            "studies (e.g., BFOR study) have demonstrated that screening unselected "
            "Ashkenazi women identifies carriers who would be missed by family history-"
            "based criteria, and is cost-effective for cancer prevention."
        ),
        "references": [
            "Levy-Lahad E et al., Proc Natl Acad Sci 1997;94:4772-4775",
            "Manchanda R et al., J Clin Oncol 2015;33:3963-3972",
        ],
    },
    # ── Additional coverage ────────────────────────────────
    {
        "id": "DOC-016",
        "title": "PIK3CA Mutations in Breast Cancer",
        "type": "variant_annotation",
        "gene": "PIK3CA",
        "content": (
            "PIK3CA encodes the p110α catalytic subunit of PI3Kα. Hotspot mutations "
            "E545K (exon 9) and H1047R (exon 20) are found in ~35% of HR+ breast "
            "cancers. These activating mutations drive AKT-mTOR signaling independent "
            "of upstream receptor activation. Alpelisib (PI3Kα-selective inhibitor) "
            "combined with fulvestrant is approved for PIK3CA-mutant HR+/HER2− "
            "advanced breast cancer. Hyperglycemia is the main toxicity due to "
            "disruption of insulin signaling via PI3Kα in metabolic tissues."
        ),
        "references": [
            "André F et al., N Engl J Med 2019;380:1929-1940",
            "Samuels Y et al., Science 2004;304:554",
        ],
    },
    {
        "id": "DOC-017",
        "title": "Lynch Syndrome and Mismatch Repair Deficiency",
        "type": "clinical",
        "gene": "MLH1",
        "content": (
            "Lynch syndrome is caused by germline mutations in mismatch repair (MMR) "
            "genes — MLH1, MSH2, MSH6, PMS2. Loss of MMR leads to microsatellite "
            "instability (MSI-H) and a hypermutator phenotype. Affected individuals "
            "have elevated risks for colorectal (50-80%), endometrial (40-60%), and "
            "other cancers. MSI-H/dMMR tumors respond well to PD-1 blockade; "
            "pembrolizumab has a tissue-agnostic approval for this biomarker."
        ),
        "references": [
            "Le DT et al., N Engl J Med 2015;372:2509-2520",
            "Møller P et al., Genet Med 2017;19:328-336",
        ],
    },
    {
        "id": "DOC-018",
        "title": "BRAF V600E and Targeted Therapy",
        "type": "therapeutic",
        "gene": "BRAF",
        "content": (
            "The BRAF V600E mutation constitutively activates the MAPK pathway and is "
            "found in ~50% of melanomas, ~10% of colorectal cancers, and various other "
            "tumors. Vemurafenib and dabrafenib (BRAF inhibitors) combined with "
            "trametinib (MEK inhibitor) are standard in BRAF-mutant melanoma. In CRC, "
            "BRAF inhibition alone is ineffective due to feedback EGFR reactivation; "
            "the triplet of encorafenib + binimetinib + cetuximab is now approved. "
            "Resistance commonly arises through RAS mutations, BRAF amplification, "
            "or MAP2K1 mutations."
        ),
        "references": [
            "Chapman PB et al., N Engl J Med 2011;364:2507-2516",
            "Kopetz S et al., N Engl J Med 2019;381:1632-1643",
        ],
    },
    {
        "id": "DOC-019",
        "title": "Liquid Biopsy and ctDNA in Cancer Monitoring",
        "type": "technology",
        "gene": "multi",
        "content": (
            "Circulating tumor DNA (ctDNA) analysis enables non-invasive detection "
            "of somatic mutations, copy number alterations, and methylation changes "
            "from a blood draw. Applications include treatment response monitoring, "
            "minimal residual disease (MRD) detection, and resistance mutation tracking. "
            "Sensitivity depends on tumor shedding rate and varies by cancer type — "
            "high in metastatic NSCLC/CRC, lower in brain tumors. FDA-approved tests "
            "include Guardant360 and FoundationOne Liquid CDx."
        ),
        "references": [
            "Wan JCM et al., Nat Rev Cancer 2017;17:223-238",
            "Chabon JJ et al., Nature 2020;580:245-251",
        ],
    },
    {
        "id": "DOC-020",
        "title": "HER2 Amplification and Antibody-Drug Conjugates",
        "type": "therapeutic",
        "gene": "ERBB2",
        "content": (
            "HER2 (ERBB2) amplification occurs in ~20% of breast cancers and ~3-5% "
            "of gastric, NSCLC, and other tumors. Trastuzumab deruxtecan (T-DXd) is "
            "an antibody-drug conjugate that has transformed HER2-targeted therapy, "
            "showing activity in HER2-low tumors (IHC 1+ or 2+/FISH−) where traditional "
            "anti-HER2 agents were ineffective. Its bystander effect through membrane-"
            "permeable payload delivery extends cytotoxicity to neighboring HER2-negative "
            "cells in the tumor microenvironment."
        ),
        "references": [
            "Modi S et al., N Engl J Med 2022;387:9-20",
            "Slamon DJ et al., N Engl J Med 2001;344:783-792",
        ],
    },
]


def get_all_documents():
    """Return all documents. Used to build the index on startup."""
    return GENOMIC_KNOWLEDGE_BASE


def get_document_by_id(doc_id: str):
    """Fetch a single document by its ID."""
    for doc in GENOMIC_KNOWLEDGE_BASE:
        if doc["id"] == doc_id:
            return doc
    return None
