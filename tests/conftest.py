import logging
import os
import sys

import pytest
import xmltodict


@pytest.fixture(name="logger")
def logger(tmp_path) -> logging.Logger:
    """
    Synthesizes a log object for testing.

    Returns
    -------
    log: logging.Logger
    """
    log_filename: str = os.path.join(tmp_path, "testing.log")
    logger = logging.getLogger(log_filename)

    # Logging to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter(
        "%(module)s - %(levelname)s - %(funcName)s - %(message)s"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Logging to a file
    logfile_format = logging.Formatter(
        fmt="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logfile_handler = logging.FileHandler(log_filename)
    logfile_handler.setFormatter(logfile_format)
    logger.addHandler(logfile_handler)

    logger.setLevel(logging.DEBUG)
    return logger


@pytest.fixture(name="fake_pmid_response")
def pmid_response() -> str:
    return """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE eSearchResult PUBLIC "-//NLM//DTD esearch 20060628//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20060628/esearch.dtd">
<eSearchResult>
    <Count>4</Count>
    <RetMax>3</RetMax>
    <RetStart>1</RetStart>
    <IdList>
        <Id>41651011</Id>
        <Id>41649907</Id>
        <Id>41351263</Id>
    </IdList>
    <TranslationSet>
        <Translation>
            <From>Allison Matthew A[Author]</From>
            <To>Allison, Matthew A[Full Author Name] OR allison matthew a[Author]</To>
        </Translation>
    </TranslationSet>
    <QueryTranslation>(allison, matthew a[Author] OR allison matthew a[Author]) AND 2026/01/01:2026/12/31[Date - Publication]</QueryTranslation>
</eSearchResult>"""


@pytest.fixture(name="empty_pmid_response")
def pmid_response_empty() -> str:
    return """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE eSearchResult PUBLIC "-//NLM//DTD esearch 20060628//EN" "https://eutils.ncbi.nlm.nih.gov/eutils/dtd/20060628/esearch.dtd">
<eSearchResult>
    <Count>0</Count>
    <RetMax>0</RetMax>
    <RetStart>1</RetStart>
    <IdList/>
    <TranslationSet>
        <Translation>
            <From>Allison Matthew A[Author]</From>
            <To>Allison, Matthew A[Full Author Name] OR allison matthew a[Author]</To>
        </Translation>
    </TranslationSet>
    <QueryTranslation>(allison, matthew a[Author] OR allison matthew a[Author]) AND 2026/01/01:2026/12/31[Date - Publication]</QueryTranslation>
</eSearchResult>"""


@pytest.fixture(name="fake_pmid_dict")
def pmid_dict(fake_pmid_response) -> dict:
    return xmltodict.parse(fake_pmid_response)


@pytest.fixture(name="fake_pubmed_response_one_article")
def pubmed_response() -> str:
    response: str = """<?xml version="1.0" ?>
<!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2025//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_250101.dtd">
<PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation Status="PubMed-not-MEDLINE" Owner="NLM">
            <PMID Version="1">41960023</PMID>
            <DateCompleted>
                <Year>2026</Year>
                <Month>04</Month>
                <Day>10</Day>
            </DateCompleted>
            <DateRevised>
                <Year>2026</Year>
                <Month>04</Month>
                <Day>10</Day>
            </DateRevised>
            <Article PubModel="Electronic-eCollection">
                <Journal>
                    <ISSN IssnType="Electronic">2471-1403</ISSN>
                    <JournalIssue CitedMedium="Internet">
                        <Volume>10</Volume>
                        <Issue>4</Issue>
                        <PubDate>
                            <Year>2026</Year>
                            <Month>Apr</Month>
                        </PubDate>
                    </JournalIssue>
                    <Title>GeoHealth</Title>
                    <ISOAbbreviation>Geohealth</ISOAbbreviation>
                </Journal>
                <ArticleTitle>Building Youth Capacity for Climate-Health Science: Lessons From Implementing The DataJam in Jordan.</ArticleTitle>
                <Pagination>
                    <StartPage>e2026GH001834</StartPage>
                    <MedlinePgn>e2026GH001834</MedlinePgn>
                </Pagination>
                <ELocationID EIdType="pii" ValidYN="Y">e2026GH001834</ELocationID>
                <ELocationID EIdType="doi" ValidYN="Y">10.1029/2026GH001834</ELocationID>
                <Abstract>
                    <AbstractText>Addressing impacts on human health from climate change will require engaged communities capable of co-creating actionable science. This is particularly the case in Jordan, one of the most vulnerable countries to climate change with a hot, dry climate and rapidly growing population. A key demographic for building capacity to address climate-health challenges is youth. To engage Jordanian youth in developing knowledge and skills related to climate-health science, the Global Center on Climate Change and Water Energy Food Health Systems (GC3WEFH) implemented The DataJam, an annual project-based data science learning program and competition developed in the United States. The GC3WEFH enrolled 87 students from 21 schools in The DataJam Jordan. Fifty-four students in teams of three completed 18 projects over a 2-year period while 33 students started The DataJam but did not complete a project. The aim of the intervention was to build data science capacity to address issues at the intersection of climate and health. To explore the outcomes of this intervention, we used the Consolidated Framework for Implementation Research to identify the primary determinants. This analysis revealed that the complexity of The DataJam and the work infrastructure of the implementation impacted communication across the intervention, which shaped the topics students researched and their use of data science. Importantly, the DataJam increased both the confidence and interest of students in engaging in climate change related challenges facing their communities. Therefore, The DataJam is a positive example of engaging youth through the international translation of a STEM learning program.</AbstractText>
                    <CopyrightInformation>&#xa9; 2026. The Author(s). GeoHealth published by Wiley Periodicals LLC on behalf of American Geophysical Union.</CopyrightInformation>
                </Abstract>
                <AuthorList CompleteYN="Y">
                    <Author ValidYN="Y">
                        <LastName>Nielsen</LastName>
                        <ForeName>Kelly</ForeName>
                        <Initials>K</Initials>
                        <Identifier Source="ORCID">0000-0001-6125-6091</Identifier>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Cameron</LastName>
                        <ForeName>Judy</ForeName>
                        <Initials>J</Initials>
                        <AffiliationInfo>
                            <Affiliation>University of Pittsburgh Pittsburgh PA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Salahat</LastName>
                        <ForeName>Mohammed</ForeName>
                        <Initials>M</Initials>
                        <Identifier Source="ORCID">0000-0001-7180-1946</Identifier>
                        <AffiliationInfo>
                            <Affiliation>Department of Land Management and Environment Prince El Hassan Bin Talal Faculty of Natural Resources and Environment The Hashemite University Zarqa Jordan.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Cramer</LastName>
                        <ForeName>Catherine</ForeName>
                        <Initials>C</Initials>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Gonzalez</LastName>
                        <ForeName>Nathan</ForeName>
                        <Initials>N</Initials>
                        <Identifier Source="ORCID">0000-0001-7518-4754</Identifier>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Al-Shurafat</LastName>
                        <ForeName>Alham</ForeName>
                        <Initials>A</Initials>
                        <AffiliationInfo>
                            <Affiliation>North Carolina State University Raleigh NC USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Alshneikat</LastName>
                        <ForeName>Lamees</ForeName>
                        <Initials>L</Initials>
                        <Identifier Source="ORCID">0009-0007-1410-3149</Identifier>
                        <AffiliationInfo>
                            <Affiliation>The Hashemite University Zarqa Jordan.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Loomis</LastName>
                        <ForeName>Debbie</ForeName>
                        <Initials>D</Initials>
                        <Identifier Source="ORCID">0009-0003-5409-4436</Identifier>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Al-Delaimy</LastName>
                        <ForeName>Wael</ForeName>
                        <Initials>W</Initials>
                        <Identifier Source="ORCID">0000-0001-8292-0510</Identifier>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                </AuthorList>
                <Language>eng</Language>
                <PublicationTypeList>
                    <PublicationType UI="D016428">Journal Article</PublicationType>
                </PublicationTypeList>
                <ArticleDate DateType="Electronic">
                    <Year>2026</Year>
                    <Month>04</Month>
                    <Day>08</Day>
                </ArticleDate>
            </Article>
            <MedlineJournalInfo>
                <Country>United States</Country>
                <MedlineTA>Geohealth</MedlineTA>
                <NlmUniqueID>101706476</NlmUniqueID>
                <ISSNLinking>2471-1403</ISSNLinking>
            </MedlineJournalInfo>
            <OtherAbstract Type="plain-language-summary" Language="eng">
                <AbstractText>Building young people's capacity to engage in science at the intersection of climate change and human health can contribute to knowledge and interventions that are more likely to be adopted and sustained. The Global Center on Climate Change and Water Energy Food Health Systems engaged Jordanian high school students using The DataJam, a project&#x2010;based data science learning program and competition developed in the United States. This study analyzed the effectiveness of The DataJam in Jordan for engaging youth in climate&#x2010;health science using data science. After showing projects tended not to focus on the intersection of climate change and health and some projects did not include data science, we employed the Consolidated Framework for Implementation Science to identify the aspects of the implementation that impacted the outcomes. We found the complexity of The DataJam and the organization of the intervention led to communication challenges throughout the process. Despite these challenges, students reported a positive experience that resulted in greater interest in climate&#x2010;health science and confidence in their ability to be engaged in their communities.</AbstractText>
                <CopyrightInformation>&#xa9; 2026. The Author(s). GeoHealth published by Wiley Periodicals LLC on behalf of American Geophysical Union.</CopyrightInformation>
            </OtherAbstract>
            <KeywordList Owner="NOTNLM">
                <Keyword MajorTopicYN="N">climate change</Keyword>
                <Keyword MajorTopicYN="N">community engagement</Keyword>
                <Keyword MajorTopicYN="N">health</Keyword>
                <Keyword MajorTopicYN="N">implementation science</Keyword>
                <Keyword MajorTopicYN="N">informal STEM</Keyword>
                <Keyword MajorTopicYN="N">youth</Keyword>
            </KeywordList>
            <CoiStatement>The authors declare no conflicts of interest relevant to this study.</CoiStatement>
        </MedlineCitation>
        <PubmedData>
            <History>
                <PubMedPubDate PubStatus="received">
                    <Year>2026</Year>
                    <Month>1</Month>
                    <Day>21</Day>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="revised">
                    <Year>2026</Year>
                    <Month>3</Month>
                    <Day>13</Day>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="accepted">
                    <Year>2026</Year>
                    <Month>3</Month>
                    <Day>18</Day>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="medline">
                    <Year>2026</Year>
                    <Month>4</Month>
                    <Day>10</Day>
                    <Hour>6</Hour>
                    <Minute>34</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="pubmed">
                    <Year>2026</Year>
                    <Month>4</Month>
                    <Day>10</Day>
                    <Hour>6</Hour>
                    <Minute>33</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="entrez">
                    <Year>2026</Year>
                    <Month>4</Month>
                    <Day>10</Day>
                    <Hour>5</Hour>
                    <Minute>38</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="pmc-release">
                    <Year>2026</Year>
                    <Month>4</Month>
                    <Day>8</Day>
                </PubMedPubDate>
            </History>
            <PublicationStatus>epublish</PublicationStatus>
            <ArticleIdList>
                <ArticleId IdType="pubmed">41960023</ArticleId>
                <ArticleId IdType="pmc">PMC13058814</ArticleId>
                <ArticleId IdType="doi">10.1029/2026GH001834</ArticleId>
                <ArticleId IdType="pii">GH270132</ArticleId>
            </ArticleIdList>
            <ReferenceList>
                <Reference>
                    <Citation>Al&#x2010;Addous, M. , Bdour, M. , Alnaief, M. , Rabaiah, S. , &amp; Schweimanns, N. (2023). Water resources in Jordan: A review of current challenges and future opportunities. Water, 15(21), 3729. 10.3390/w15213729</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3390/w15213729</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Beier, P. , Hansen, L. J. , Halbrecht, L. , &amp; Behar, D. (2016). A how&#x2010;to guide for coproduction of actionable science. Conservation Letters, 10(3), 288&#x2013;296. 10.1111/conl.12300</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1111/conl.12300</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Chambers, J. M. , Wyborn, C. , Ryan, M. E. , Reid, R. S. , Riechers, M. , Serban, A. , et&#xa0;al. (2021). Six modes of co&#x2010;production for sustainability. Nature Sustainability, 4(11), 983&#x2013;996. 10.1038/s41893-021-00755-x</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1038/s41893-021-00755-x</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Clark, W. C. , van Kerkhoff, L. , Lebel, L. , &amp; Gallopin, G. C. (2016). Crafting usable knowledge for sustainable development. Sustainability Science, 113(17), 4570&#x2013;4578. 10.1073/pnas.1601266113</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1073/pnas.1601266113</ArticleId>
                        <ArticleId IdType="pmc">PMC4855559</ArticleId>
                        <ArticleId IdType="pubmed">27091979</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Clemens, V. , von Hirschhausen, E. , &amp; Fegert, J. M. (2022). Report of the intergovernmental panel on climate change: Implications for the mental health policy of children and adolescents in Europe&#x2014;A scoping review. European Child &amp; Adolescent Psychiatry, 31(5), 701&#x2013;713. 10.1007/s00787-020-01615-3</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s00787-020-01615-3</ArticleId>
                        <ArticleId IdType="pmc">PMC9142437</ArticleId>
                        <ArticleId IdType="pubmed">32845381</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Culha, D. (2016). Applying competition&#x2010;based learning to agile software engineering. Computer Applications in Engineering Education, 24, 382&#x2013;387. 10.1002/cae.21716</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1002/cae.21716</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Damschroder, L. J. , Aron, D. C. , Keith, R. E. , Kirsh, S. R. , Alexander, J. A. , &amp; Lowery, J. C. (2009). Fostering implementation of health services research findings into practice: A consolidated framework for advancing implementation science. Implementation Science, 4(1), 50. 10.1186/1748-5908-4-50</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/1748-5908-4-50</ArticleId>
                        <ArticleId IdType="pmc">PMC2736161</ArticleId>
                        <ArticleId IdType="pubmed">19664226</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Desiderio, E. , Garcia&#x2010;Herrero, L. , Hall, D. , Pertot, I. , Segre, A. , &amp; Vittuari, M. (2024). From youth engagement to policy insights: Identifying and testing food systems' sustainability indicators. Environmental Science &amp; Policy, 155, 103718. 10.1016/j.envsci.2024.103718</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.envsci.2024.103718</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Fuster, M. , Dimond, E. , Handley, M. A. , Rose, D. , Stoecker, C. , Knapp, M. , et&#xa0;al. (2023). Evaluating the outcomes and implementation determinants of interventions co&#x2010;developed using human&#x2010;centered design to promote healthy eating in restaurants: An application of the consolidated framework for implementation research. Frontiers in Public Health, 11, 1150790. 10.3389/fpubh.2023.1150790</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3389/fpubh.2023.1150790</ArticleId>
                        <ArticleId IdType="pmc">PMC10233011</ArticleId>
                        <ArticleId IdType="pubmed">37275479</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>

Gasparri, G.
, 
Omrani, O. E.
, 
Hinton, R.
, 
Imbago, D.
, 
Lakhani, H.
, 
Mohan, A.
, et&#xa0;al. (2021). Children, adolescents, and youth pioneering a human rights&#x2010;based approach to climate change. Health and Human Rights Journal, 23(2), 95&#x2013;108. https://pubmed.ncbi.nlm.nih.gov/34966228/
</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="pmc">PMC8694303</ArticleId>
                        <ArticleId IdType="pubmed">34966228</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>
Generation Unlimited
. (2025). Green rising: Mobilizing millions of young people to protect their communities from the climate crisis. Retrieved from https://www.generationunlimited.org/green&#x2010;rising
</Citation>
                </Reference>
                <Reference>
                    <Citation>Gerlak, A. K. , Guido, Z. , Owen, G. , McGoffin, M. S. R. , Louder, E. , Davies, J. , et&#xa0;al. (2023). Stakeholder engagement in the co&#x2010;production of knowledge for environmental decision&#x2010;making. World Development, 170, 106336. 10.1016/j.worlddev.2023.106336</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.worlddev.2023.106336</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Haqqi, S. , Soorjamurthi, S. , Macdonald, B. , Begandy, C. , Cameron, J. , Pirollo, B. , et al. (2018). DataJam: Introducing high school students to data science. In ITiCSE 2018: Proceedings of the 23rd Annual ACM Conference on Innovation and Technology in Computer Science Education (p.&#xa0;387). 10.1145/3197091.3205812</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1145/3197091.3205812</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Harvey, B. , Cochrane, L. , &amp; Van Epp, M. (2019). Charting knowledge co&#x2010;production pathways in climate and development. Environmental Policy and Governance, 29(2), 107&#x2013;117. 10.1002/eet.1834</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1002/eet.1834</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Harvey, B. , Huang, Y. , Araujo, J. , Vincent, K. , Roux, J. , Rouhaud, E. , &amp; Visman, E. (2021). Mobilizing climate information for decision&#x2010;making in Africa: Contrasting user&#x2010;centered and knowledge&#x2010;centered approaches. Frontiers in Climate, 2, 589282. 10.3389/fclim.2020.589282</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3389/fclim.2020.589282</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Kerins, C. , McHugh, S. , McSharry, J. , Reardon, C. M. , Hayes, C. , Perry, I. J. , et&#xa0;al. (2020). Barriers and facilitators to implementation of menu labelling interventions from a food service industry perspective: A mixed methods systematic review. International Journal of Behavioral Nutrition and Physical Activity, 17(1), 48. 10.1186/s12966-020-00948-1</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s12966-020-00948-1</ArticleId>
                        <ArticleId IdType="pmc">PMC7161210</ArticleId>
                        <ArticleId IdType="pubmed">32295647</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Khosravi, M. , Mojtabaeian, S. M. , &amp; Sarvestani, M. A. (2024). A systematic review on the outcomes of climate change in the Middle&#x2010;Eastern countries: The catastrophes of Yemen and Syria. Environmental Health Insights, 18, 11786302241302270. 10.1177/11786302241302270</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1177/11786302241302270</ArticleId>
                        <ArticleId IdType="pmc">PMC11645776</ArticleId>
                        <ArticleId IdType="pubmed">39679384</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Kirk, M. A. , Kelley, C. , Yankey, N. , Birken, S. A. , Abadie, B. , &amp; Damschroder, L. (2016). A systematic review of the use of the Consolidated Framework for Implementation Research. Implementation Science, 11(1), 72. 10.1186/s13012-016-0437-z</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s13012-016-0437-z</ArticleId>
                        <ArticleId IdType="pmc">PMC4869309</ArticleId>
                        <ArticleId IdType="pubmed">27189233</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Lee, Y. , &amp; Lee, B. (2024). Developing career&#x2010;related skills through project&#x2010;based learning. Studies in Educational Evaluation, 83, 101378. 10.1016/j.stueduc.2024.101378</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.stueduc.2024.101378</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Mach, K. J. , Lemos, M. C. , Meadow, A. M. , Wyborn, C. , Klenk, N. , Arnott, J. C. , et&#xa0;al. (2020). Actionable knowledge and the art of engagement. Current Opinion in Environmental Sustainability, 42, 30&#x2013;37. 10.1016/j.cosust.2020.01.002</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.cosust.2020.01.002</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Malafaia, C. , Diogenes&#x2010;Lima, J. , Pereira, B. , Macedo, E. , &amp; Menezes, I. (2024). Collaborative climate labs: A youth&#x2010;led methodology for co&#x2010;creating community responses to climate change. Research in Education, 121(2), 192&#x2013;216. 10.1177/00345237241288407</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1177/00345237241288407</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Maslin, M. , Ramnath, R. D. , Welsh, G. I. , &amp; Sisodiya, S. M. (2025). Understanding the health impacts of the climate crisis. Future Healthcare Journal, 12(1), 100240. 10.1016/j.fhj.2025.100240</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.fhj.2025.100240</ArticleId>
                        <ArticleId IdType="pmc">PMC11998295</ArticleId>
                        <ArticleId IdType="pubmed">40236934</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Neira, M. , Erguler, K. , Ahmady&#x2010;Birgani, H. , Al&#x2010;Hmoud, N. D. , Fears, R. , Gogos, C. , et&#xa0;al. (2023). Climate change and human health in the Eastern Mediterranean and Middle East: Literature review, research priorities and policy suggestions. Environmental Research, 216(2), 114537. 10.1016/j.envres.2022.114537</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.envres.2022.114537</ArticleId>
                        <ArticleId IdType="pmc">PMC9729515</ArticleId>
                        <ArticleId IdType="pubmed">36273599</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Parth, S. , Schickl, M. , Oberauer, K. , Kuish, S. , Deisenrieder, V. , Liebhaber, N. , et al. (2024). Teenagers performing research on climate change education in a fully integrated design&#x2010;based research setting. International Journal of Science Education, 46(10), 978&#x2013;1000. 10.1080/09500693.2023.2268295</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1080/09500693.2023.2268295</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Reed, M. S. (2008). Stakeholder participation for environmental management: A literature review. Biological Conservation, 141(10), 2417&#x2013;2431. 10.1016/j.biocon.2008.07.014</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.biocon.2008.07.014</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Sanson, A. V. , Van Hoorn, J. , &amp; Burke, S. E. L. (2019). Responding to the impacts of the climate crisis on children and youth. Child Development Perspectives, 13(4), 201&#x2013;207. 10.1111/cdep.12342</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1111/cdep.12342</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Stavrianakis, K. , Nielsen, J. A. E. , &amp; Morrison, Z. (2025). Climate change projects and youth engagement: Empowerment and contested knowledge. Sustainability, 17(16), 7556. 10.3390/su17167556</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3390/su17167556</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Talley, J. L. , Schneider, J. , &amp; Lindquist, E. (2016). A simplified approach to stakeholder engagement in natural resource management: The Five&#x2010;Feature Framework. Ecology &amp; Society, 21(4), 38. 10.5751/ES-08830-210438</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.5751/ES-08830-210438</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Thew, H. (2018). Youth participation and agency in the United Nations framework convention on climate change. International Environmental Agreements: Politics, Law, and Economics, 18(3), 369&#x2013;389. 10.1007/s10784-018-9392-2</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s10784-018-9392-2</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Thew, H. , Middlemiss, L. , &amp; Paavola, J. (2020). &#x201c;Youth is not a political position&#x201d;: Exploring justice claims&#x2010;making in UN Climate Change Negotiations. Global Environmental Change, 61, 102036. 10.1016/j.gloenvcha.2020.102036</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.gloenvcha.2020.102036</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Tilt, J. , Babbar&#x2010;Sebens, M. , Ramadas, M. , Kolagani, N. , &amp; Naren, U. S. (2024). Participatory framing of a conceptual decision model for a hyperlocalized food, energy, and water nexus: A case study in adaptive management of rural water systems in India. Journal of Water Resources Planning and Management, 150(4), 1&#x2013;13. 10.1061/JWRMD5.WRENG-6154</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1061/JWRMD5.WRENG-6154</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Trott, C. D. , Weinberg, A. E. , Frame, S. M. , Jean&#x2010;Pierre, P. , &amp; Even, T. L. (2023). Civic science education for youth&#x2010;driven water security: A behavioral development approach to strengthening climate resilience. International Journal of Behavioral Development, 48(2), 145&#x2013;155. 10.1177/01650254231188661</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1177/01650254231188661</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Worker, S. M. , Espinoza, D. , Kok, C. M. , Neas, S. , &amp; Smith, M. H. (2023). Youth participatory action research: Integrating science learning and civic engagement. California Agriculture, 77(2), 74&#x2013;82. 10.3733/ca.2023a0009</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3733/ca.2023a0009</ArticleId>
                    </ArticleIdList>
                </Reference>
            </ReferenceList>
        </PubmedData>
    </PubmedArticle>
</PubmedArticleSet>"""
    return response


@pytest.fixture(name="fake_pubmed_dict_one_article")
def pubmed_dict(fake_pubmed_response_one_article) -> dict:
    return xmltodict.parse(fake_pubmed_response_one_article)


@pytest.fixture(name="fake_pubmed_response_two_articles")
def pubmed_response_two_articles() -> str:
    return """<?xml version="1.0" ?>
<!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2025//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_250101.dtd">
<PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation Status="PubMed-not-MEDLINE" Owner="NLM">
            <PMID Version="1">41960023</PMID>
            <DateCompleted>
                <Year>2026</Year>
                <Month>04</Month>
                <Day>10</Day>
            </DateCompleted>
            <DateRevised>
                <Year>2026</Year>
                <Month>04</Month>
                <Day>10</Day>
            </DateRevised>
            <Article PubModel="Electronic-eCollection">
                <Journal>
                    <ISSN IssnType="Electronic">2471-1403</ISSN>
                    <JournalIssue CitedMedium="Internet">
                        <Volume>10</Volume>
                        <Issue>4</Issue>
                        <PubDate>
                            <Year>2026</Year>
                            <Month>Apr</Month>
                        </PubDate>
                    </JournalIssue>
                    <Title>GeoHealth</Title>
                    <ISOAbbreviation>Geohealth</ISOAbbreviation>
                </Journal>
                <ArticleTitle>Building Youth Capacity for Climate-Health Science: Lessons From Implementing The DataJam in Jordan.</ArticleTitle>
                <Pagination>
                    <StartPage>e2026GH001834</StartPage>
                    <MedlinePgn>e2026GH001834</MedlinePgn>
                </Pagination>
                <ELocationID EIdType="pii" ValidYN="Y">e2026GH001834</ELocationID>
                <ELocationID EIdType="doi" ValidYN="Y">10.1029/2026GH001834</ELocationID>
                <Abstract>
                    <AbstractText>Addressing impacts on human health from climate change will require engaged communities capable of co-creating actionable science. This is particularly the case in Jordan, one of the most vulnerable countries to climate change with a hot, dry climate and rapidly growing population. A key demographic for building capacity to address climate-health challenges is youth. To engage Jordanian youth in developing knowledge and skills related to climate-health science, the Global Center on Climate Change and Water Energy Food Health Systems (GC3WEFH) implemented The DataJam, an annual project-based data science learning program and competition developed in the United States. The GC3WEFH enrolled 87 students from 21 schools in The DataJam Jordan. Fifty-four students in teams of three completed 18 projects over a 2-year period while 33 students started The DataJam but did not complete a project. The aim of the intervention was to build data science capacity to address issues at the intersection of climate and health. To explore the outcomes of this intervention, we used the Consolidated Framework for Implementation Research to identify the primary determinants. This analysis revealed that the complexity of The DataJam and the work infrastructure of the implementation impacted communication across the intervention, which shaped the topics students researched and their use of data science. Importantly, the DataJam increased both the confidence and interest of students in engaging in climate change related challenges facing their communities. Therefore, The DataJam is a positive example of engaging youth through the international translation of a STEM learning program.</AbstractText>
                    <CopyrightInformation>&#xa9; 2026. The Author(s). GeoHealth published by Wiley Periodicals LLC on behalf of American Geophysical Union.</CopyrightInformation>
                </Abstract>
                <AuthorList CompleteYN="Y">
                    <Author ValidYN="Y">
                        <LastName>Nielsen</LastName>
                        <ForeName>Kelly</ForeName>
                        <Initials>K</Initials>
                        <Identifier Source="ORCID">0000-0001-6125-6091</Identifier>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Cameron</LastName>
                        <ForeName>Judy</ForeName>
                        <Initials>J</Initials>
                        <AffiliationInfo>
                            <Affiliation>University of Pittsburgh Pittsburgh PA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Salahat</LastName>
                        <ForeName>Mohammed</ForeName>
                        <Initials>M</Initials>
                        <Identifier Source="ORCID">0000-0001-7180-1946</Identifier>
                        <AffiliationInfo>
                            <Affiliation>Department of Land Management and Environment Prince El Hassan Bin Talal Faculty of Natural Resources and Environment The Hashemite University Zarqa Jordan.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Cramer</LastName>
                        <ForeName>Catherine</ForeName>
                        <Initials>C</Initials>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Gonzalez</LastName>
                        <ForeName>Nathan</ForeName>
                        <Initials>N</Initials>
                        <Identifier Source="ORCID">0000-0001-7518-4754</Identifier>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Al-Shurafat</LastName>
                        <ForeName>Alham</ForeName>
                        <Initials>A</Initials>
                        <AffiliationInfo>
                            <Affiliation>North Carolina State University Raleigh NC USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Alshneikat</LastName>
                        <ForeName>Lamees</ForeName>
                        <Initials>L</Initials>
                        <Identifier Source="ORCID">0009-0007-1410-3149</Identifier>
                        <AffiliationInfo>
                            <Affiliation>The Hashemite University Zarqa Jordan.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Loomis</LastName>
                        <ForeName>Debbie</ForeName>
                        <Initials>D</Initials>
                        <Identifier Source="ORCID">0009-0003-5409-4436</Identifier>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Al-Delaimy</LastName>
                        <ForeName>Wael</ForeName>
                        <Initials>W</Initials>
                        <Identifier Source="ORCID">0000-0001-8292-0510</Identifier>
                        <AffiliationInfo>
                            <Affiliation>University of California San Diego La Jolla CA USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                </AuthorList>
                <Language>eng</Language>
                <PublicationTypeList>
                    <PublicationType UI="D016428">Journal Article</PublicationType>
                </PublicationTypeList>
                <ArticleDate DateType="Electronic">
                    <Year>2026</Year>
                    <Month>04</Month>
                    <Day>08</Day>
                </ArticleDate>
            </Article>
            <MedlineJournalInfo>
                <Country>United States</Country>
                <MedlineTA>Geohealth</MedlineTA>
                <NlmUniqueID>101706476</NlmUniqueID>
                <ISSNLinking>2471-1403</ISSNLinking>
            </MedlineJournalInfo>
            <OtherAbstract Type="plain-language-summary" Language="eng">
                <AbstractText>Building young people's capacity to engage in science at the intersection of climate change and human health can contribute to knowledge and interventions that are more likely to be adopted and sustained. The Global Center on Climate Change and Water Energy Food Health Systems engaged Jordanian high school students using The DataJam, a project&#x2010;based data science learning program and competition developed in the United States. This study analyzed the effectiveness of The DataJam in Jordan for engaging youth in climate&#x2010;health science using data science. After showing projects tended not to focus on the intersection of climate change and health and some projects did not include data science, we employed the Consolidated Framework for Implementation Science to identify the aspects of the implementation that impacted the outcomes. We found the complexity of The DataJam and the organization of the intervention led to communication challenges throughout the process. Despite these challenges, students reported a positive experience that resulted in greater interest in climate&#x2010;health science and confidence in their ability to be engaged in their communities.</AbstractText>
                <CopyrightInformation>&#xa9; 2026. The Author(s). GeoHealth published by Wiley Periodicals LLC on behalf of American Geophysical Union.</CopyrightInformation>
            </OtherAbstract>
            <KeywordList Owner="NOTNLM">
                <Keyword MajorTopicYN="N">climate change</Keyword>
                <Keyword MajorTopicYN="N">community engagement</Keyword>
                <Keyword MajorTopicYN="N">health</Keyword>
                <Keyword MajorTopicYN="N">implementation science</Keyword>
                <Keyword MajorTopicYN="N">informal STEM</Keyword>
                <Keyword MajorTopicYN="N">youth</Keyword>
            </KeywordList>
            <CoiStatement>The authors declare no conflicts of interest relevant to this study.</CoiStatement>
        </MedlineCitation>
        <PubmedData>
            <History>
                <PubMedPubDate PubStatus="received">
                    <Year>2026</Year>
                    <Month>1</Month>
                    <Day>21</Day>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="revised">
                    <Year>2026</Year>
                    <Month>3</Month>
                    <Day>13</Day>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="accepted">
                    <Year>2026</Year>
                    <Month>3</Month>
                    <Day>18</Day>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="medline">
                    <Year>2026</Year>
                    <Month>4</Month>
                    <Day>10</Day>
                    <Hour>6</Hour>
                    <Minute>34</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="pubmed">
                    <Year>2026</Year>
                    <Month>4</Month>
                    <Day>10</Day>
                    <Hour>6</Hour>
                    <Minute>33</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="entrez">
                    <Year>2026</Year>
                    <Month>4</Month>
                    <Day>10</Day>
                    <Hour>5</Hour>
                    <Minute>38</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="pmc-release">
                    <Year>2026</Year>
                    <Month>4</Month>
                    <Day>8</Day>
                </PubMedPubDate>
            </History>
            <PublicationStatus>epublish</PublicationStatus>
            <ArticleIdList>
                <ArticleId IdType="pubmed">41960023</ArticleId>
                <ArticleId IdType="pmc">PMC13058814</ArticleId>
                <ArticleId IdType="doi">10.1029/2026GH001834</ArticleId>
                <ArticleId IdType="pii">GH270132</ArticleId>
            </ArticleIdList>
            <ReferenceList>
                <Reference>
                    <Citation>Al&#x2010;Addous, M. , Bdour, M. , Alnaief, M. , Rabaiah, S. , &amp; Schweimanns, N. (2023). Water resources in Jordan: A review of current challenges and future opportunities. Water, 15(21), 3729. 10.3390/w15213729</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3390/w15213729</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Beier, P. , Hansen, L. J. , Halbrecht, L. , &amp; Behar, D. (2016). A how&#x2010;to guide for coproduction of actionable science. Conservation Letters, 10(3), 288&#x2013;296. 10.1111/conl.12300</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1111/conl.12300</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Chambers, J. M. , Wyborn, C. , Ryan, M. E. , Reid, R. S. , Riechers, M. , Serban, A. , et&#xa0;al. (2021). Six modes of co&#x2010;production for sustainability. Nature Sustainability, 4(11), 983&#x2013;996. 10.1038/s41893-021-00755-x</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1038/s41893-021-00755-x</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Clark, W. C. , van Kerkhoff, L. , Lebel, L. , &amp; Gallopin, G. C. (2016). Crafting usable knowledge for sustainable development. Sustainability Science, 113(17), 4570&#x2013;4578. 10.1073/pnas.1601266113</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1073/pnas.1601266113</ArticleId>
                        <ArticleId IdType="pmc">PMC4855559</ArticleId>
                        <ArticleId IdType="pubmed">27091979</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Clemens, V. , von Hirschhausen, E. , &amp; Fegert, J. M. (2022). Report of the intergovernmental panel on climate change: Implications for the mental health policy of children and adolescents in Europe&#x2014;A scoping review. European Child &amp; Adolescent Psychiatry, 31(5), 701&#x2013;713. 10.1007/s00787-020-01615-3</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s00787-020-01615-3</ArticleId>
                        <ArticleId IdType="pmc">PMC9142437</ArticleId>
                        <ArticleId IdType="pubmed">32845381</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Culha, D. (2016). Applying competition&#x2010;based learning to agile software engineering. Computer Applications in Engineering Education, 24, 382&#x2013;387. 10.1002/cae.21716</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1002/cae.21716</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Damschroder, L. J. , Aron, D. C. , Keith, R. E. , Kirsh, S. R. , Alexander, J. A. , &amp; Lowery, J. C. (2009). Fostering implementation of health services research findings into practice: A consolidated framework for advancing implementation science. Implementation Science, 4(1), 50. 10.1186/1748-5908-4-50</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/1748-5908-4-50</ArticleId>
                        <ArticleId IdType="pmc">PMC2736161</ArticleId>
                        <ArticleId IdType="pubmed">19664226</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Desiderio, E. , Garcia&#x2010;Herrero, L. , Hall, D. , Pertot, I. , Segre, A. , &amp; Vittuari, M. (2024). From youth engagement to policy insights: Identifying and testing food systems' sustainability indicators. Environmental Science &amp; Policy, 155, 103718. 10.1016/j.envsci.2024.103718</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.envsci.2024.103718</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Fuster, M. , Dimond, E. , Handley, M. A. , Rose, D. , Stoecker, C. , Knapp, M. , et&#xa0;al. (2023). Evaluating the outcomes and implementation determinants of interventions co&#x2010;developed using human&#x2010;centered design to promote healthy eating in restaurants: An application of the consolidated framework for implementation research. Frontiers in Public Health, 11, 1150790. 10.3389/fpubh.2023.1150790</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3389/fpubh.2023.1150790</ArticleId>
                        <ArticleId IdType="pmc">PMC10233011</ArticleId>
                        <ArticleId IdType="pubmed">37275479</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>

Gasparri, G.
, 
Omrani, O. E.
, 
Hinton, R.
, 
Imbago, D.
, 
Lakhani, H.
, 
Mohan, A.
, et&#xa0;al. (2021). Children, adolescents, and youth pioneering a human rights&#x2010;based approach to climate change. Health and Human Rights Journal, 23(2), 95&#x2013;108. https://pubmed.ncbi.nlm.nih.gov/34966228/
</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="pmc">PMC8694303</ArticleId>
                        <ArticleId IdType="pubmed">34966228</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>
Generation Unlimited
. (2025). Green rising: Mobilizing millions of young people to protect their communities from the climate crisis. Retrieved from https://www.generationunlimited.org/green&#x2010;rising
</Citation>
                </Reference>
                <Reference>
                    <Citation>Gerlak, A. K. , Guido, Z. , Owen, G. , McGoffin, M. S. R. , Louder, E. , Davies, J. , et&#xa0;al. (2023). Stakeholder engagement in the co&#x2010;production of knowledge for environmental decision&#x2010;making. World Development, 170, 106336. 10.1016/j.worlddev.2023.106336</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.worlddev.2023.106336</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Haqqi, S. , Soorjamurthi, S. , Macdonald, B. , Begandy, C. , Cameron, J. , Pirollo, B. , et al. (2018). DataJam: Introducing high school students to data science. In ITiCSE 2018: Proceedings of the 23rd Annual ACM Conference on Innovation and Technology in Computer Science Education (p.&#xa0;387). 10.1145/3197091.3205812</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1145/3197091.3205812</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Harvey, B. , Cochrane, L. , &amp; Van Epp, M. (2019). Charting knowledge co&#x2010;production pathways in climate and development. Environmental Policy and Governance, 29(2), 107&#x2013;117. 10.1002/eet.1834</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1002/eet.1834</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Harvey, B. , Huang, Y. , Araujo, J. , Vincent, K. , Roux, J. , Rouhaud, E. , &amp; Visman, E. (2021). Mobilizing climate information for decision&#x2010;making in Africa: Contrasting user&#x2010;centered and knowledge&#x2010;centered approaches. Frontiers in Climate, 2, 589282. 10.3389/fclim.2020.589282</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3389/fclim.2020.589282</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Kerins, C. , McHugh, S. , McSharry, J. , Reardon, C. M. , Hayes, C. , Perry, I. J. , et&#xa0;al. (2020). Barriers and facilitators to implementation of menu labelling interventions from a food service industry perspective: A mixed methods systematic review. International Journal of Behavioral Nutrition and Physical Activity, 17(1), 48. 10.1186/s12966-020-00948-1</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s12966-020-00948-1</ArticleId>
                        <ArticleId IdType="pmc">PMC7161210</ArticleId>
                        <ArticleId IdType="pubmed">32295647</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Khosravi, M. , Mojtabaeian, S. M. , &amp; Sarvestani, M. A. (2024). A systematic review on the outcomes of climate change in the Middle&#x2010;Eastern countries: The catastrophes of Yemen and Syria. Environmental Health Insights, 18, 11786302241302270. 10.1177/11786302241302270</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1177/11786302241302270</ArticleId>
                        <ArticleId IdType="pmc">PMC11645776</ArticleId>
                        <ArticleId IdType="pubmed">39679384</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Kirk, M. A. , Kelley, C. , Yankey, N. , Birken, S. A. , Abadie, B. , &amp; Damschroder, L. (2016). A systematic review of the use of the Consolidated Framework for Implementation Research. Implementation Science, 11(1), 72. 10.1186/s13012-016-0437-z</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s13012-016-0437-z</ArticleId>
                        <ArticleId IdType="pmc">PMC4869309</ArticleId>
                        <ArticleId IdType="pubmed">27189233</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Lee, Y. , &amp; Lee, B. (2024). Developing career&#x2010;related skills through project&#x2010;based learning. Studies in Educational Evaluation, 83, 101378. 10.1016/j.stueduc.2024.101378</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.stueduc.2024.101378</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Mach, K. J. , Lemos, M. C. , Meadow, A. M. , Wyborn, C. , Klenk, N. , Arnott, J. C. , et&#xa0;al. (2020). Actionable knowledge and the art of engagement. Current Opinion in Environmental Sustainability, 42, 30&#x2013;37. 10.1016/j.cosust.2020.01.002</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.cosust.2020.01.002</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Malafaia, C. , Diogenes&#x2010;Lima, J. , Pereira, B. , Macedo, E. , &amp; Menezes, I. (2024). Collaborative climate labs: A youth&#x2010;led methodology for co&#x2010;creating community responses to climate change. Research in Education, 121(2), 192&#x2013;216. 10.1177/00345237241288407</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1177/00345237241288407</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Maslin, M. , Ramnath, R. D. , Welsh, G. I. , &amp; Sisodiya, S. M. (2025). Understanding the health impacts of the climate crisis. Future Healthcare Journal, 12(1), 100240. 10.1016/j.fhj.2025.100240</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.fhj.2025.100240</ArticleId>
                        <ArticleId IdType="pmc">PMC11998295</ArticleId>
                        <ArticleId IdType="pubmed">40236934</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Neira, M. , Erguler, K. , Ahmady&#x2010;Birgani, H. , Al&#x2010;Hmoud, N. D. , Fears, R. , Gogos, C. , et&#xa0;al. (2023). Climate change and human health in the Eastern Mediterranean and Middle East: Literature review, research priorities and policy suggestions. Environmental Research, 216(2), 114537. 10.1016/j.envres.2022.114537</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.envres.2022.114537</ArticleId>
                        <ArticleId IdType="pmc">PMC9729515</ArticleId>
                        <ArticleId IdType="pubmed">36273599</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Parth, S. , Schickl, M. , Oberauer, K. , Kuish, S. , Deisenrieder, V. , Liebhaber, N. , et al. (2024). Teenagers performing research on climate change education in a fully integrated design&#x2010;based research setting. International Journal of Science Education, 46(10), 978&#x2013;1000. 10.1080/09500693.2023.2268295</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1080/09500693.2023.2268295</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Reed, M. S. (2008). Stakeholder participation for environmental management: A literature review. Biological Conservation, 141(10), 2417&#x2013;2431. 10.1016/j.biocon.2008.07.014</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.biocon.2008.07.014</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Sanson, A. V. , Van Hoorn, J. , &amp; Burke, S. E. L. (2019). Responding to the impacts of the climate crisis on children and youth. Child Development Perspectives, 13(4), 201&#x2013;207. 10.1111/cdep.12342</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1111/cdep.12342</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Stavrianakis, K. , Nielsen, J. A. E. , &amp; Morrison, Z. (2025). Climate change projects and youth engagement: Empowerment and contested knowledge. Sustainability, 17(16), 7556. 10.3390/su17167556</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3390/su17167556</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Talley, J. L. , Schneider, J. , &amp; Lindquist, E. (2016). A simplified approach to stakeholder engagement in natural resource management: The Five&#x2010;Feature Framework. Ecology &amp; Society, 21(4), 38. 10.5751/ES-08830-210438</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.5751/ES-08830-210438</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Thew, H. (2018). Youth participation and agency in the United Nations framework convention on climate change. International Environmental Agreements: Politics, Law, and Economics, 18(3), 369&#x2013;389. 10.1007/s10784-018-9392-2</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s10784-018-9392-2</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Thew, H. , Middlemiss, L. , &amp; Paavola, J. (2020). &#x201c;Youth is not a political position&#x201d;: Exploring justice claims&#x2010;making in UN Climate Change Negotiations. Global Environmental Change, 61, 102036. 10.1016/j.gloenvcha.2020.102036</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.gloenvcha.2020.102036</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Tilt, J. , Babbar&#x2010;Sebens, M. , Ramadas, M. , Kolagani, N. , &amp; Naren, U. S. (2024). Participatory framing of a conceptual decision model for a hyperlocalized food, energy, and water nexus: A case study in adaptive management of rural water systems in India. Journal of Water Resources Planning and Management, 150(4), 1&#x2013;13. 10.1061/JWRMD5.WRENG-6154</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1061/JWRMD5.WRENG-6154</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Trott, C. D. , Weinberg, A. E. , Frame, S. M. , Jean&#x2010;Pierre, P. , &amp; Even, T. L. (2023). Civic science education for youth&#x2010;driven water security: A behavioral development approach to strengthening climate resilience. International Journal of Behavioral Development, 48(2), 145&#x2013;155. 10.1177/01650254231188661</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1177/01650254231188661</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Worker, S. M. , Espinoza, D. , Kok, C. M. , Neas, S. , &amp; Smith, M. H. (2023). Youth participatory action research: Integrating science learning and civic engagement. California Agriculture, 77(2), 74&#x2013;82. 10.3733/ca.2023a0009</Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3733/ca.2023a0009</ArticleId>
                    </ArticleIdList>
                </Reference>
            </ReferenceList>
        </PubmedData>
    </PubmedArticle>
    <PubmedArticle>
        <MedlineCitation Status="PubMed-not-MEDLINE" Owner="NLM">
            <PMID Version="1">41873419</PMID>
            <DateCompleted>
                <Year>2026</Year>
                <Month>03</Month>
                <Day>24</Day>
            </DateCompleted>
            <DateRevised>
                <Year>2026</Year>
                <Month>03</Month>
                <Day>24</Day>
            </DateRevised>
            <Article PubModel="Electronic-eCollection">
                <Journal>
                    <ISSN IssnType="Print">1177-889X</ISSN>
                    <JournalIssue CitedMedium="Print">
                        <Volume>20</Volume>
                        <PubDate>
                            <Year>2026</Year>
                        </PubDate>
                    </JournalIssue>
                    <Title>Patient preference and adherence</Title>
                    <ISOAbbreviation>Patient Prefer Adherence</ISOAbbreviation>
                </Journal>
                <ArticleTitle>Public Perceptions of Ethical and Professional Practice in Jordanian Community Pharmacies: A Cross-Sectional Study.</ArticleTitle>
                <Pagination>
                    <StartPage>578660</StartPage>
                    <MedlinePgn>578660</MedlinePgn>
                </Pagination>
                <ELocationID EIdType="pii" ValidYN="Y">578660</ELocationID>
                <ELocationID EIdType="doi" ValidYN="Y">10.2147/PPA.S578660</ELocationID>
                <Abstract>
                    <AbstractText Label="BACKGROUND" NlmCategory="UNASSIGNED">Ethical and professional pharmacy practice is fundamental to supporting patient safety and trust. Despite advances in Good Pharmacy Practice (GPP), evidence from developing systems indicates gaps in ethical performance. This study aimed to assess the ethical dimensions of community pharmacists' practice in Jordan from the public's perspective, focusing on counseling quality, privacy, autonomy, and fairness.</AbstractText>
                    <AbstractText Label="METHODS" NlmCategory="UNASSIGNED">A cross-sectional survey was conducted among 710 community pharmacy clients across Jordan using a validated questionnaire measured five ethical domains and an attitude scale. Composite scores for patient satisfaction, ethical conduct, and pharmacist attitude were calculated. Descriptive statistics and logistic regression were used to identify demographic predictors.</AbstractText>
                    <AbstractText Label="RESULTS" NlmCategory="UNASSIGNED">Participants were predominantly female (57.9%) and from central Jordan (69.6%). Mean domain scores were: history-taking (51.3 &#xb1; 34.3), counseling (60.3 &#xb1; 29.6), privacy (67.8 &#xb1; 26.1), autonomy (60.2 &#xb1; 36.6), and justice (86.5 &#xb1; 24.0). Counseling was strongest for medication use and timing but weakest for safety aspects-adverse effects (41.4%), storage (40.1%), and drug interactions (31.7%). Justice and professionalism received the highest perception scores, while privacy and autonomy received moderate ratings. Gender (female) and south region predicted higher satisfaction and ethical perception (
                        <i>p</i> &lt; 0.05).
                    </AbstractText>
                    <AbstractText Label="CONCLUSION" NlmCategory="UNASSIGNED">Community pharmacists in Jordan were perceived as demonstrating strong fairness and professionalism, but gaps remain in safety-oriented counseling and privacy assurance. These findings highlight areas where communication practices, privacy infrastructure, and ethics-oriented training may warrant further attention. Strengthening these areas could contribute to supporting patient trust and the ethical quality of community pharmacy services.</AbstractText>
                    <CopyrightInformation>&#xa9; 2026 Jarad et al.</CopyrightInformation>
                </Abstract>
                <AuthorList CompleteYN="Y">
                    <Author ValidYN="Y" EqualContrib="Y">
                        <LastName>Jarad</LastName>
                        <ForeName>Ola F</ForeName>
                        <Initials>OF</Initials>
                        <AffiliationInfo>
                            <Affiliation>Department of Clinical Pharmacy, Faculty of Pharmacy, Jordan University of Science and Technology, Irbid, Jordan.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y" EqualContrib="Y">
                        <LastName>Hasan</LastName>
                        <ForeName>Hisham E</ForeName>
                        <Initials>HE</Initials>
                        <Identifier Source="ORCID">0000-0001-6513-2037</Identifier>
                        <AffiliationInfo>
                            <Affiliation>Department of Clinical Pharmacy, Faculty of Pharmacy, Jordan University of Science and Technology, Irbid, Jordan.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Khabour</LastName>
                        <ForeName>Omar F</ForeName>
                        <Initials>OF</Initials>
                        <Identifier Source="ORCID">0000-0002-3006-3104</Identifier>
                        <AffiliationInfo>
                            <Affiliation>Department of Medical Laboratory Sciences, Faculty of Applied Medical Sciences, Jordan University of Science and Technology, Irbid, Jordan.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Alzoubi</LastName>
                        <ForeName>Karem H</ForeName>
                        <Initials>KH</Initials>
                        <Identifier Source="ORCID">0000-0002-2808-5099</Identifier>
                        <AffiliationInfo>
                            <Affiliation>Department of Pharmaceutical Sciences, College of Pharmacy, QU Health, Qatar University, Doha, Qatar.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                    <Author ValidYN="Y">
                        <LastName>Al-Delaimy</LastName>
                        <ForeName>Wael K</ForeName>
                        <Initials>WK</Initials>
                        <AffiliationInfo>
                            <Affiliation>Herbert Wertheim School of Public Health and Human Longevity Science, University of California, San Diego, La Jolla, CA, USA.</Affiliation>
                        </AffiliationInfo>
                    </Author>
                </AuthorList>
                <Language>eng</Language>
                <PublicationTypeList>
                    <PublicationType UI="D016428">Journal Article</PublicationType>
                </PublicationTypeList>
                <ArticleDate DateType="Electronic">
                    <Year>2026</Year>
                    <Month>03</Month>
                    <Day>18</Day>
                </ArticleDate>
            </Article>
            <MedlineJournalInfo>
                <Country>New Zealand</Country>
                <MedlineTA>Patient Prefer Adherence</MedlineTA>
                <NlmUniqueID>101475748</NlmUniqueID>
                <ISSNLinking>1177-889X</ISSNLinking>
            </MedlineJournalInfo>
            <KeywordList Owner="NOTNLM">
                <Keyword MajorTopicYN="N">Jordan</Keyword>
                <Keyword MajorTopicYN="N">community pharmacy</Keyword>
                <Keyword MajorTopicYN="N">patient counselling</Keyword>
                <Keyword MajorTopicYN="N">patient-centered care</Keyword>
                <Keyword MajorTopicYN="N">pharmaceutical ethics</Keyword>
                <Keyword MajorTopicYN="N">professional conduct</Keyword>
            </KeywordList>
            <CoiStatement>The authors declare that there is no conflict of interest.</CoiStatement>
        </MedlineCitation>
        <PubmedData>
            <History>
                <PubMedPubDate PubStatus="received">
                    <Year>2025</Year>
                    <Month>11</Month>
                    <Day>3</Day>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="accepted">
                    <Year>2026</Year>
                    <Month>2</Month>
                    <Day>13</Day>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="medline">
                    <Year>2026</Year>
                    <Month>3</Month>
                    <Day>24</Day>
                    <Hour>7</Hour>
                    <Minute>42</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="pubmed">
                    <Year>2026</Year>
                    <Month>3</Month>
                    <Day>24</Day>
                    <Hour>7</Hour>
                    <Minute>41</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="entrez">
                    <Year>2026</Year>
                    <Month>3</Month>
                    <Day>24</Day>
                    <Hour>3</Hour>
                    <Minute>47</Minute>
                </PubMedPubDate>
                <PubMedPubDate PubStatus="pmc-release">
                    <Year>2026</Year>
                    <Month>3</Month>
                    <Day>18</Day>
                </PubMedPubDate>
            </History>
            <PublicationStatus>epublish</PublicationStatus>
            <ArticleIdList>
                <ArticleId IdType="pubmed">41873419</ArticleId>
                <ArticleId IdType="pmc">PMC13005987</ArticleId>
                <ArticleId IdType="doi">10.2147/PPA.S578660</ArticleId>
                <ArticleId IdType="pii">578660</ArticleId>
            </ArticleIdList>
            <ReferenceList>
                <Reference>
                    <Citation>Wang Y, Rao Y, Yin Y, Li Y, Lin Z, Zhang B. A bibliometric analysis of global trends in the research field of pharmaceutical care over the past 20 years. 
                        <i>Front Public Health</i>. 2022;10:980866. doi: 10.3389/fpubh.2022.980866
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3389/fpubh.2022.980866</ArticleId>
                        <ArticleId IdType="pmc">PMC9618714</ArticleId>
                        <ArticleId IdType="pubmed">36324463</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Grabenweger R, V&#xf6;lz D, Weck C, Hau P, Paal P, Bumes E. Spirituality in professional patient-centered care for adults with primary brain tumors: an exploratory scoping review. 
                        <i>J Religion Health</i>. 2025;64(3):2165&#x2013;15. doi: 10.1007/s10943-024-02161-x
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s10943-024-02161-x</ArticleId>
                        <ArticleId IdType="pmc">PMC12133965</ArticleId>
                        <ArticleId IdType="pubmed">39500854</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Olson AW, Vaidyanathan R, Stratton TP, Isetts BJ, Hillman LA, Schommer JC. Patient-centered care preferences &amp; expectations in outpatient pharmacist practice: a three archetype heuristic. 
                        <i>Res Soc Administrative Pharm</i>. 2021;17(10):1820&#x2013;1830. doi: 10.1016/j.sapharm.2021.02.005
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.sapharm.2021.02.005</ArticleId>
                        <ArticleId IdType="pubmed">33582079</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Roosan D, Wu Y, Tatla V, et al. Framework to enable pharmacist access to health care data using blockchain technology and artificial intelligence. 
                        <i>J Am Pharm Assoc</i>. 2022;62(4):1124&#x2013;1132. doi: 10.1016/j.japh.2022.02.018
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.japh.2022.02.018</ArticleId>
                        <ArticleId IdType="pubmed">35307309</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Shea M. The ethics of clinical ethics. 
                        <i>HEC forum</i>. 2025;37(3):389&#x2013;410. doi: 10.1007/s10730-024-09544-3
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s10730-024-09544-3</ArticleId>
                        <ArticleId IdType="pmc">PMC12313721</ArticleId>
                        <ArticleId IdType="pubmed">39611879</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Herzanych VM, Badyda AY, Buletsa NV, Svyshcho VY. Ethical and legal principles of biomedical research. 
                        <i>Wiadomosci Lekarskie</i>. 2025;78(4):943&#x2013;948. doi: 10.36740/WLek/203907
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.36740/WLek/203907</ArticleId>
                        <ArticleId IdType="pubmed">40367482</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Seedhouse D. 
                        <i>People-Centred Pharmacy: Ethical Challenges in Everyday Practice</i>. John Wiley &amp; Sons; 2025.
                    </Citation>
                </Reference>
                <Reference>
                    <Citation>Kusynov&#xe1; Z, van den Ham HA, Leufkens HGM, Mantel-Teeuwisse AK. Longitudinal study of good pharmacy practice roles covered at the annual world pharmacy congresses 2003-2019. 
                        <i>J Pharm Policy Pract</i>. 2022;15(1):94. doi: 10.1186/s40545-022-00482-4
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s40545-022-00482-4</ArticleId>
                        <ArticleId IdType="pmc">PMC9706975</ArticleId>
                        <ArticleId IdType="pubmed">36443800</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Jairoun AA, Al-Hemyari SS, Shahwan M, et al. Top unresolved ethical challenges and dilemmas faced by community pharmacists in providing pharmaceutical care: drawing the line between ethical challenges and the quality of the pharmaceutical care. 
                        <i>Res Soc Administrative Pharm</i>. 2022;18(10):3711&#x2013;3713. doi: 10.1016/j.sapharm.2022.05.009
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.sapharm.2022.05.009</ArticleId>
                        <ArticleId IdType="pubmed">35618648</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Esmalipour R, Larijani B, Mehrdad N, Ebadi A, Salari P. The ethical challenges in pharmacy practice in community pharmacies: a qualitative study. 
                        <i>Saudi Pharm J</i>. 2021;29(12):1441&#x2013;1448. doi: 10.1016/j.jsps.2021.11.003
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.jsps.2021.11.003</ArticleId>
                        <ArticleId IdType="pmc">PMC8720823</ArticleId>
                        <ArticleId IdType="pubmed">35002382</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Wernecke K, Nadolny S, Schildmann J, Schiek S, Bertsche T. Ethical conflicts in patient care situations of community pharmacists: a cross-sectional online survey. 
                        <i>Int J Clin Pharm</i>. 2024;46(6):1500&#x2013;1513. doi: 10.1007/s11096-024-01797-9
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s11096-024-01797-9</ArticleId>
                        <ArticleId IdType="pmc">PMC11576625</ArticleId>
                        <ArticleId IdType="pubmed">39240277</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Akour A, Halloush S, Nusair MB, Barakat M, Abdulla F, Al Momani M. Gaps in pharmaceutical care for patients with mental health issues: a cross-sectional study. 
                        <i>Int J Clin Pharm</i>. 2022;44(4):904&#x2013;913. doi: 10.1007/s11096-022-01391-x
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s11096-022-01391-x</ArticleId>
                        <ArticleId IdType="pmc">PMC8974808</ArticleId>
                        <ArticleId IdType="pubmed">35364752</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Hasan HE, Jaber D, Khabour OF, Alzoubi KH. Ethical considerations and concerns in the implementation of AI in pharmacy practice: a cross-sectional study. 
                        <i>BMC Med Ethics</i>. 2024;25(1):55. doi: 10.1186/s12910-024-01062-8
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s12910-024-01062-8</ArticleId>
                        <ArticleId IdType="pmc">PMC11096093</ArticleId>
                        <ArticleId IdType="pubmed">38750441</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Al-Delaimy WK, Alzoubi K, Khabour O, Jaber S. Research ethics education program in Jordan: achievements and challenges. 
                        <i>J Empirical Res Human Res Ethics</i>. 2025;15562646251331757. doi: 10.1177/15562646251331757
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1177/15562646251331757</ArticleId>
                        <ArticleId IdType="pubmed">40620092</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Alnahar SA, AL-Rawashdeh AI, Makhzoomy AK, Bates I. What is needed to reform pharmacy education in Jordan: an exploratory study based on a multi-stakeholder perspective. 
                        <i>Pharm Educ</i>. 2022;22(4):63&#x2013;72. doi: 10.46542/pe.2022.224.6372
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.46542/pe.2022.224.6372</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Pharmacy ACoC. Standards of practice for clinical pharmacists. 
                        <i>J Am College Clin Pharm</i>. 2023;6(10):1156&#x2013;1159. doi: 10.1002/jac5.1873
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1002/jac5.1873</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Hayakawa M, Kizaki H, Yanagisawa Y, et al. Development of a novel person-centered question prompt list to talk with your pharmacists in Japanese community pharmacies: focus group and Delphi method. 
                        <i>J Pharm Health Care Sci</i>. 2025;11(1):87. doi: 10.1186/s40780-025-00494-7
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s40780-025-00494-7</ArticleId>
                        <ArticleId IdType="pmc">PMC12522932</ArticleId>
                        <ArticleId IdType="pubmed">41088474</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Bloom TJ, Kebodeaux C, Munger M, Smith MD, Stutz M, Wagner J. A narrative review of pharmacy identity and the PharmD experiment. 
                        <i>Am J Pharm Educ</i>. 2025;89(2):101351. doi: 10.1016/j.ajpe.2024.101351
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.ajpe.2024.101351</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Hasan HE. Review of ethics in pharmacy practice: a practical guide. In: Sullivan DM, C. Douglas C, Anderson JWC, editors. 
                        <i>Ethics in Pharmacy Practice: A Practical Guide</i>. Switzerland: Springer Nature; 2021. ISBN 978&#x2013;3-030&#x2013;72171-8.
                    </Citation>
                </Reference>
                <Reference>
                    <Citation>Alghamdi KS, Petzold M, Ewis AA, Alsugoor MH, Saaban K, Hussain-Alkhateeb L. Public perspective toward extended community pharmacy services in sub-national Saudi Arabia: an online cross-sectional study. 
                        <i>PLoS One</i>. 2023;18(10):e0280095. doi: 10.1371/journal.pone.0280095
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1371/journal.pone.0280095</ArticleId>
                        <ArticleId IdType="pmc">PMC10553341</ArticleId>
                        <ArticleId IdType="pubmed">37796778</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Owusu YB, Abouelhassan R, Awaisu A. Evaluation of patient safety culture in community pharmacies in Qatar. 
                        <i>Int J Clin Pract</i>. 2021;75(5):e14055. doi: 10.1111/ijcp.14055
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1111/ijcp.14055</ArticleId>
                        <ArticleId IdType="pubmed">33527626</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Alsaleh FM, Abahussain EA, Altabaa HH, Al-Bazzaz MF, Almandil NB. Assessment of patient safety culture: a nationwide survey of community pharmacists in Kuwait. 
                        <i>BMC Health Serv Res</i>. 2018;18(1):884. doi: 10.1186/s12913-018-3662-0
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s12913-018-3662-0</ArticleId>
                        <ArticleId IdType="pmc">PMC6251142</ArticleId>
                        <ArticleId IdType="pubmed">30466436</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Fino LB, Basheti IA, Chaar BB. Exploring ethical pharmacy practice in Jordan. 
                        <i>Sci Engineer Ethics</i>. 2020;26(5):2809&#x2013;2834. doi: 10.1007/s11948-020-00231-3
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s11948-020-00231-3</ArticleId>
                        <ArticleId IdType="pubmed">32533448</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Basheti IA, Mhaidat NM, Alqudah R, Nassar R, Othman B, Mukattash TL. Primary health care policy and vision for community pharmacy and pharmacists in Jordan. 
                        <i>Pharm Pract</i>. 2020;18(4):2184. doi: 10.18549/PharmPract.2020.4.2184
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.18549/PharmPract.2020.4.2184</ArticleId>
                        <ArticleId IdType="pmc">PMC7732212</ArticleId>
                        <ArticleId IdType="pubmed">33343774</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Salari P, Namazi H, Abdollahi M, et al. Code of ethics for the national pharmaceutical system: codifying and compilation. 
                        <i>J Res Med Sci</i>. 2013;18(5):442&#x2013;448.
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="pmc">PMC3810583</ArticleId>
                        <ArticleId IdType="pubmed">24174954</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Blenkinsopp A, Duerden M, Blenkinsopp J. 
                        <i>Symptoms in the Pharmacy: A Guide to the Management of Common Illnesses and Disease Prevention</i>. John Wiley &amp; Sons; 2025.
                    </Citation>
                </Reference>
                <Reference>
                    <Citation>Naser AY, Abu Sbeat BS. Satisfaction with community pharmacies services in Jordan: a cross-sectional study. 
                        <i>Saudi Pharm J</i>. 2022;30(11):1646&#x2013;1651. doi: 10.1016/j.jsps.2022.09.007
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1016/j.jsps.2022.09.007</ArticleId>
                        <ArticleId IdType="pmc">PMC9715631</ArticleId>
                        <ArticleId IdType="pubmed">36465853</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Al-Taani GM, Ayoub NM. Assessment of satisfaction of attendees of healthcare centers in Jordan with community pharmacy services of pharmacies they usually use. 
                        <i>PLoS One</i>. 2024;19(7):e0305991. doi: 10.1371/journal.pone.0305991
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1371/journal.pone.0305991</ArticleId>
                        <ArticleId IdType="pmc">PMC11262638</ArticleId>
                        <ArticleId IdType="pubmed">39038057</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Tindall WN, Beardsley RS, Kimberlin CL. Communication skills in pharmacy practice. A practical guide for students and practitioners. 
                        <i>Am J Hospital Pharm</i>. 1990;47(4):944&#x2013;947.
                    </Citation>
                </Reference>
                <Reference>
                    <Citation>Owens CT, Baergen R. Pharmacy practice in high-volume community settings: barriers and ethical responsibilities. 
                        <i>Pharmacy</i>. 2021;9(2). doi: 10.3390/pharmacy9020074
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3390/pharmacy9020074</ArticleId>
                        <ArticleId IdType="pmc">PMC8167746</ArticleId>
                        <ArticleId IdType="pubmed">33916737</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Varkey B. Principles of clinical ethics and their application to practice. 
                        <i>Med Princ Pract</i>. 2021;30(1):17&#x2013;28. doi: 10.1159/000509119
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1159/000509119</ArticleId>
                        <ArticleId IdType="pmc">PMC7923912</ArticleId>
                        <ArticleId IdType="pubmed">32498071</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Ghaly M. Islamic ethical perspectives on life-sustaining treatments. 
                        <i>Eastern Mediterranean Health J</i>. 2022;27(8):557&#x2013;559. doi: 10.26719/emhj.22.044
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.26719/emhj.22.044</ArticleId>
                        <ArticleId IdType="pubmed">36134487</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Aissaoui Y, Charif F, Bencharfa B, Bouchama A, Myatt I, Belhadj A. End-of-life care in Moroccan ICUs: ethical challenges, practices, and perspectives of intensivists. 
                        <i>BMC Med Ethics</i>. 2025;26(1):135. doi: 10.1186/s12910-025-01271-9
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s12910-025-01271-9</ArticleId>
                        <ArticleId IdType="pmc">PMC12522822</ArticleId>
                        <ArticleId IdType="pubmed">41094455</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Bulus Y, Abiola T. Evidence-based practice adherence and medical error reduction: an Islamic ethical perspective. 
                        <i>Iman Med J</i>. 2025;11(1).
                    </Citation>
                </Reference>
                <Reference>
                    <Citation>Wijianto DW, Nurinnafi&#x2019;a AMU, Luthfitah A, Firdaus MW, Suryandaru S, Febriani RE. Implementation of islamic ethics in pharmaceutical services: a literature review approach. 
                        <i>Solo Int Collab Pub Soc Sci Human</i>. 2023;1(03):181&#x2013;188. doi: 10.61455/sicopus.v1i03.64
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.61455/sicopus.v1i03.64</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Schoenthaler A, Knafl GJ, Fiscella K, Ogedegbe G. Addressing the social needs of hypertensive patients: the role of patient&#x2013;provider communication as a predictor of medication adherence. 
                        <i>Circ Cardiovasc Qual Outcomes</i>. 2017;10(9):e003659. doi: 10.1161/CIRCOUTCOMES.117.003659
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1161/CIRCOUTCOMES.117.003659</ArticleId>
                        <ArticleId IdType="pmc">PMC5571828</ArticleId>
                        <ArticleId IdType="pubmed">28830861</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>DiPiro JT, Talbert RL, Yee GC, Matzke GR, Wells BG, Posey LM. Pharmacotherapy: a pathophysiologic approach. 2014.</Citation>
                </Reference>
                <Reference>
                    <Citation>Iroegbu C, Tuot DS, Lewis L, Matura LA. The influence of patient-provider communication on self-management among patients with chronic illness: a systematic mixed studies review. 
                        <i>J Adv Nurs</i>. 2025;81(4):1678&#x2013;1699. doi: 10.1111/jan.16492
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1111/jan.16492</ArticleId>
                        <ArticleId IdType="pmc">PMC11896829</ArticleId>
                        <ArticleId IdType="pubmed">39340765</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Mukattash TL, Bazzi NH, Nuseir KQ, Jarab AS, Abu-Farha RK, Khdour MR. Pharmaceutical care in community pharmacies in Jordan: a public survey. 
                        <i>Pharm Pract</i>. 2018;16(2):1126. doi: 10.18549/PharmPract.2018.02.1126
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.18549/PharmPract.2018.02.1126</ArticleId>
                        <ArticleId IdType="pmc">PMC6041206</ArticleId>
                        <ArticleId IdType="pubmed">30023022</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Easwaran V, Almeleebia TM, Mantargi MJS, et al. Patient safety culture in the southern region of Saudi Arabia: a survey among community pharmacies. 
                        <i>Healthcare</i>. 2023;11(10):1416.
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="pmc">PMC10218386</ArticleId>
                        <ArticleId IdType="pubmed">37239699</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Mohamed S, Palaian S, Alomar M, M M-A-A. A national survey on community pharmacists&#x2019; perception, practice and perceived barriers towards pharmaceutical care services in the United Arab Emirates. 
                        <i>J Pharm Policy Pract</i>. 2025;18(1):2523936. doi: 10.1080/20523211.2025.2523936
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1080/20523211.2025.2523936</ArticleId>
                        <ArticleId IdType="pmc">PMC12239235</ArticleId>
                        <ArticleId IdType="pubmed">40636561</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Alameddine M, Bou-Karroum K, Hijazi MA. A national study on the resilience of community pharmacists in Lebanon: a cross-sectional survey. 
                        <i>J Pharm Policy Pract</i>. 2022;15(1):8. doi: 10.1186/s40545-022-00406-2
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s40545-022-00406-2</ArticleId>
                        <ArticleId IdType="pmc">PMC8795943</ArticleId>
                        <ArticleId IdType="pubmed">35090571</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Alameddine M, Bou-Karroum K, Kassas S, Hijazi MA. A profession in danger: stakeholders&#x2019; perspectives on supporting the pharmacy profession in Lebanon. 
                        <i>PLoS One</i>. 2020;15(11):e0242213. doi: 10.1371/journal.pone.0242213
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1371/journal.pone.0242213</ArticleId>
                        <ArticleId IdType="pmc">PMC7668569</ArticleId>
                        <ArticleId IdType="pubmed">33196652</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Iranmanesh M, Yazdi-Feyzabadi V, Mehrolhassani MH. The challenges of ethical behaviors for drug supply in pharmacies in Iran by a principle-based approach. 
                        <i>BMC Med Ethics</i>. 2020;21(1):84. doi: 10.1186/s12910-020-00531-0
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s12910-020-00531-0</ArticleId>
                        <ArticleId IdType="pmc">PMC7466816</ArticleId>
                        <ArticleId IdType="pubmed">32873312</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Nahar P, Unicomb L, Lucas PJ, et al. What contributes to inappropriate antibiotic dispensing among qualified and unqualified healthcare providers in Bangladesh? A qualitative study. 
                        <i>BMC Health Serv Res</i>. 2020;20(1):656. doi: 10.1186/s12913-020-05512-y
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s12913-020-05512-y</ArticleId>
                        <ArticleId IdType="pmc">PMC7362537</ArticleId>
                        <ArticleId IdType="pubmed">32669092</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Ahmed WS, Nebeker C. Assessment of research ethics education offerings of pharmacy master programs in an Arab nation relative to top programs worldwide: a qualitative content analysis. 
                        <i>PLoS One</i>. 2021;16(2):e0238755. doi: 10.1371/journal.pone.0238755
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1371/journal.pone.0238755</ArticleId>
                        <ArticleId IdType="pmc">PMC7895361</ArticleId>
                        <ArticleId IdType="pubmed">33606694</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Ahmed WS, Ahmed A, Alzoubi KH, Nebeker C. Perceptions of pharmacy graduate students toward research ethics education: a cross-sectional study from a developing country. 
                        <i>Sci Engineer Ethics</i>. 2022;28(6):47. doi: 10.1007/s11948-022-00406-0
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s11948-022-00406-0</ArticleId>
                        <ArticleId IdType="pmc">PMC9606090</ArticleId>
                        <ArticleId IdType="pubmed">36287276</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>ElKhalifa D, Hussein O, Hamid A, Al-Ziftawi N, Al-Hashimi I, Ibrahim MIM. Curriculum, competency development, and assessment methods of MSc and PhD pharmacy programs: a scoping review. 
                        <i>BMC Med Educ</i>. 2024;24(1):989. doi: 10.1186/s12909-024-05820-5
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1186/s12909-024-05820-5</ArticleId>
                        <ArticleId IdType="pmc">PMC11391760</ArticleId>
                        <ArticleId IdType="pubmed">39261860</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Alameri M, Al-Taani G, Alsous M, Shilbayeh S, Al Mazrouei N. Attitude and awareness toward general and professional ethics among pharmacists and pharmacy students: a cross-sectional study from Jordan. 
                        <i>Healthcare</i>. 2025;13(13). doi: 10.3390/healthcare13131556
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.3390/healthcare13131556</ArticleId>
                        <ArticleId IdType="pmc">PMC12250506</ArticleId>
                        <ArticleId IdType="pubmed">40648580</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>McBane S, Alavandi P, Allen S, et al. Overview of implementation and learning outcomes of simulation in pharmacy education. 
                        <i>J Am College Clin Pharm</i>. 2023;6(5):528&#x2013;554. doi: 10.1002/jac5.1784
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1002/jac5.1784</ArticleId>
                    </ArticleIdList>
                </Reference>
                <Reference>
                    <Citation>Peh KQE, Kwan YH, Goh H, et al. An adaptable framework for factors contributing to medication adherence: results from a systematic review of 102 conceptual frameworks. 
                        <i>J Gen Intern Med</i>. 2021;36(9):2784&#x2013;2795. doi: 10.1007/s11606-021-06648-1
                    </Citation>
                    <ArticleIdList>
                        <ArticleId IdType="doi">10.1007/s11606-021-06648-1</ArticleId>
                        <ArticleId IdType="pmc">PMC8390603</ArticleId>
                        <ArticleId IdType="pubmed">33660211</ArticleId>
                    </ArticleIdList>
                </Reference>
            </ReferenceList>
        </PubmedData>
    </PubmedArticle>
</PubmedArticleSet>"""


@pytest.fixture(name="fake_pubmed_dict_two_articles")
def pubmed_dict_two_articles(fake_pubmed_response_two_articles) -> dict:
    return xmltodict.parse(fake_pubmed_response_two_articles)


@pytest.fixture(name="sample_faculty_list")
def sample_faculty_list() -> list[str]:
    return [
        "Tai-Seale, PhD, MPH",
        "Wu, Jennifer, MD",
        "Cheng, Terri, MD",
        "Celebi, Julie, MD",
    ]


@pytest.fixture(name="username")
def user() -> str:
    return os.getlogin()
