from flask import make_response, jsonify,send_file
from flask import render_template,request,make_response
from flask_paginate import Pagination
import re,string
from SEG import app,mysql
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
@app.route("/index.bs")
def index_file():
    pos="/home/tangq/SEG/SEG/index.bs"
    return send_file(pos,mimetype='text/plain')
@app.route("/")
def index():
    return render_template("homepage.html")
@app.route("/cellline")
def cellline():
    return render_template("CCLE_cellline_tissue.html")

@app.route("/TCGAbarchart")
def TCGAbarplot():
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA'''
    # sql_count = '''SELECT id, cancer,gene,tag,miR,gene_TF,TF_target, cancer_full_name,tissue,met_number FROM TCGA'''
    curs.execute(sql_count)
    result = curs.fetchall()
    # print result
    fin = list(result)
    seg = []
    CATEGORYlist = []
    highlist = []
    lowlist = []
    dic = {}
    CAP = '<chart labelDisplay="Rotate" slantLabels="1" xAxisNamePadding="0" yAxisNamePadding="0" formatNumberScale="0" canvasBgDepth="7" plottoolText="$label{br}$seriesname gene number:$value" canvasBaseDepth="7" maxLabelHeight="300" divLineAlpha="36"  placevaluesInside="0" showValues="1" valueFontBold="0" valueFontColor="#FF00FF" caption="SEGs in TCGA" subcaption="Specifically high or low expressed gene numbers" outcnvbasefont="Arial" baseFontSize="12" plotSpacePercent="30"  outcnvbasefontsize="18" outcnvbasefontcolor="#383838" labelFontSize="12" xaxisname="Cancer type"  yaxisname="Gene numbers" palette="1" yaxismaxvalue="1100" numdivlines="3" theme="ocean"><categories>'
    for i in fin:
        id, tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,=i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]
        # id, cancer, gene, tag, miR, gene_TF, TF_target, cancer_full_name, tissue, met_number=i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]
        dic.setdefault(cancer, []).append(tag)
    key=sorted(dic.keys())
    for k in key:
        v=dic[k]
        # for k, v in dic.iteritems():
        CATEGORY = '<category label="' + str(k) + '" />'
        CATEGORYlist.append(CATEGORY)
        hi = '<set value="' + str(v.count('high')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/TCGAtables?cancer=' + str(k) + '&tag=' + 'high' + '"' + '/>'
        # hi = '<set value="' + str(v.count('high')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/TCGAtables?label=' + str(k) + '&series=' + 'high' + '"' + '/>'
        highlist.append(hi)
        lo = '<set value="' + str(v.count('low')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/TCGAtables?cancer=' + str(k) + '&tag=' + 'low' + '"' + '/>'
        lowlist.append(lo)
    TCGAbardata1=CAP + ''.join(CATEGORYlist) + '</categories>' + '<dataset seriesname="highly expressed">' + ''.join(highlist) + '</dataset>' + '<dataset seriesname="lowly expressed">' + ''.join(lowlist) + '</dataset></chart>'
    TCGAbardata=TCGAbardata1.replace("value=\"0\"","value=\"\"")
    name="TCGAbarplot"
    return render_template("barplot-TCGA.html",name=name,TCGAbardata=TCGAbardata)
@app.route("/CCLEbarchart")
def CCLEbarplot():
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Thyroid,Salivary_gland,Soft_tissue,Haematopoietic_and_lymphoid_tissue,Biliary_tract,Pancreas,Central_nervous_system,Small_intestine,Bone,Large_intestine,Autonomic_ganglia,Pleura,Urinary_tract,Lung,Breast,Skin,Ovary,Prostate,Kidney,Upper_aerodigestive_tract,Stomach,Endometrium,Oesophagus,Liver FROM CCLE'''
    curs.execute(sql_count)
    result = curs.fetchall()
    fin = list(result)
    CATEGORYlist = []
    highlist = []
    lowlist = []
    dic = {}
    CAP = '<chart labelDisplay="Rotate" slantLabels="1" xAxisNamePadding="0" yAxisNamePadding="0" formatNumberScale="0" canvasBgDepth="7" plottoolText="$label{br}$seriesname gene number:$value" canvasBaseDepth="7" maxLabelHeight="300" divLineAlpha="36"  placevaluesInside="0" showValues="1" valueFontBold="0" valueFontColor="#FF00FF" caption="SEGs in CCLE" subcaption="Specifically high or low expressed gene numbers" outcnvbasefont="Arial" baseFontSize="12" plotSpacePercent="30"  outcnvbasefontsize="18" outcnvbasefontcolor="#383838" labelFontSize="12" xaxisname="Tissue type"  yaxisname="Gene numbers" palette="1" yaxismaxvalue="1100" numdivlines="3" theme="ocean"><categories>'
    for i in fin:
        id, tissue, gene, tag, miR, TF_or_gene, gene_TF, TF_target = i[0], i[1], i[2], i[3], i[4], i[5], i[6],i[7]
        dic.setdefault(tissue, []).append(tag)
    key = sorted(dic.keys())
    for k in key:
        v = dic[k]
        # for k, v in dic.iteritems():
        CATEGORY = '<category label="' + str(k) + '" />'
        CATEGORYlist.append(CATEGORY)
        hi = '<set value="' + str(v.count('high')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/CCLEtables?tissue=' + str(k) + '&tag=' + 'high' + '"' + '/>'
        highlist.append(hi)
        lo = '<set value="' + str(v.count('low')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/CCLEtables?tissue=' + str(k) + '&tag=' + 'low' + '"' + '/>'
        lowlist.append(lo)
    CCLEbardata1 = CAP + ''.join(CATEGORYlist) + '</categories>' + '<dataset seriesname="highly expressed">' + ''.join(highlist) + '</dataset>' + '<dataset seriesname="lowly expressed">' + ''.join(lowlist) + '</dataset></chart>'
    CCLEbardata = CCLEbardata1.replace('value=\"0\"', 'value=\"\"')
    name="CCLEbarplot"
    return render_template("barplot-CCLE.html",name=name,CCLEbardata=CCLEbardata)
@app.route("/GTExbarchart")
def GTExbarplot():
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Artery,Bladder,Brain,Breast,Transformed_fibroblasts,Cervix,Colon,Esophagus,Fallopian_tube,Heart,Kidney,Liver,Lung,Salivary_gland,Muscle,Tibial_nerve,Ovary,Pancreas,Pituitary,Prostate,Skin,Small_intestine,Spleen,Stomach,Testis,Thyroid,Uterus,Vagina,Blood FROM GTEx'''
    curs.execute(sql_count)
    result = curs.fetchall()
    # print result
    fin = list(result)
    # seg = []
    CATEGORYlist = []
    highlist = []
    lowlist = []
    dic = {}
    CAP = '<chart labelDisplay="Rotate" slantLabels="1" xAxisNamePadding="0" yAxisNamePadding="0" formatNumberScale="0" canvasBgDepth="7" plottoolText="$label{br}$seriesname gene number:$value" canvasBaseDepth="7" maxLabelHeight="300" divLineAlpha="36"  placevaluesInside="0" showValues="1" valueFontBold="0" valueFontColor="#FF00FF" caption="SEGs in GTEx" subcaption="Specifically high or low expressed gene numbers" outcnvbasefont="Arial" baseFontSize="12" plotSpacePercent="30"  outcnvbasefontsize="18" outcnvbasefontcolor="#383838" labelFontSize="12" xaxisname="Tissue type"  yaxisname="Gene numbers" palette="1" yaxismaxvalue="1100" numdivlines="3" theme="ocean"><categories>'
    for i in fin:
        id, tissue, gene, tag, miR, TF_or_gene, gene_TF, TF_target = i[0], i[1], i[2], i[3], i[4], i[5], i[6],i[7]
        dic.setdefault(tissue, []).append(tag)
    key = sorted(dic.keys())
    for k in key:
        v = dic[k]
        # for k, v in dic.iteritems():
        CATEGORY = '<category label="' + str(k) + '" />'
        CATEGORYlist.append(CATEGORY)
        hi = '<set value="' + str(v.count('high')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/GTExtables?tissue=' + str(k) + '&tag=' + 'high' + '"' + '/>'
        highlist.append(hi)
        lo = '<set value="' + str(v.count('low')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/GTExtables?tissue=' + str(k) + '&tag=' + 'low' + '"' + '/>'
        lowlist.append(lo)
    GTExbardata1 = CAP + ''.join(CATEGORYlist) + '</categories>' + '<dataset seriesname="highly expressed">' + ''.join(highlist) + '</dataset>' + '<dataset seriesname="lowly expressed">' + ''.join(lowlist) + '</dataset></chart>'
    GTExbardata = GTExbardata1.replace('value=\"0\"', 'value=\"\"')
    name="GTExbarplot"
    return render_template("barplot-GTEx.html", name=name,GTExbardata=GTExbardata)
@app.route("/BodyMapbarchart")
def BodyMapbarplot():
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Duodenum,Placenta,Lung,Brain,Ovary,Thyroid,Smooth_muscle,Stomach,Endometrium,Heart,Tonsil,Salivary_gland,Breast,Cerebral_cortex,Lymph_node,Spleen,Testis,Skeletal_muscle,Small_intestine,Colon,Liver,Skin,Fallopian_tube,Rectum,Pancreas,Leukocyte,Kidney,Esophagus,Bladder,Bone_marrow,Appendix,Gall_bladder,Prostate FROM EBI'''
    curs.execute(sql_count)
    result = curs.fetchall()
    fin = list(result)
    CATEGORYlist = []
    highlist = []
    lowlist = []
    dic = {}
    CAP = '<chart labelDisplay="Rotate" slantLabels="1" xAxisNamePadding="0" yAxisNamePadding="0" formatNumberScale="0" canvasBgDepth="7" plottoolText="$label{br}$seriesname gene number:$value" canvasBaseDepth="7" maxLabelHeight="300" divLineAlpha="36"  placevaluesInside="0" showValues="1" valueFontBold="0" valueFontColor="#FF00FF" caption="SEGs in BodyMap" subcaption="Specifically high or low expressed gene numbers" outcnvbasefont="Arial" baseFontSize="12" plotSpacePercent="30"  outcnvbasefontsize="18" outcnvbasefontcolor="#383838" labelFontSize="12" xaxisname="Tissue type"  yaxisname="Gene numbers" palette="1" yaxismaxvalue="1100" numdivlines="3" theme="ocean"><categories>'
    for i in fin:
        id, tissue, gene, tag, miR, TF_or_gene, gene_TF, TF_target = i[0], i[1], i[2], i[3], i[4], i[5], i[6],i[7]
        dic.setdefault(tissue, []).append(tag)
    key = sorted(dic.keys())
    for k in key:
        v = dic[k]
        # for k, v in dic.iteritems():
        CATEGORY = '<category label="' + str(k) + '" />'
        CATEGORYlist.append(CATEGORY)
        hi = '<set value="' + str(v.count('high')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/BodyMaptables?tissue=' + str(k) + '&tag=' + 'high' + '"' + '/>'
        highlist.append(hi)
        lo = '<set value="' + str(v.count('low')) + '" ' + 'link="n-http://bioinfo.life.hust.edu.cn/SEGreg/BodyMaptables?tissue=' + str(k) + '&tag=' + 'low' + '"' + '/>'
        lowlist.append(lo)
    BodyMapbardata1 = CAP + ''.join(CATEGORYlist) + '</categories>' + '<dataset seriesname="highly expressed">' + ''.join(highlist) + '</dataset>' + '<dataset seriesname="lowly expressed">' + ''.join(lowlist) + '</dataset></chart>'
    BodyMapbardata = BodyMapbardata1.replace('value=\"0\"', 'value=\"\"')
    name="BodyMapbarplot"
    return render_template("barplot-BodyMap.html", name=name,BodyMapbardata=BodyMapbardata)


@app.route("/TCGA")
def TCGA():
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA'''
    curs.execute(sql_count)
    result = curs.fetchall()
    # print result
    genes = list(result)
    data=[]
    for i in genes:
        miR_list=[]
        i8 = "; ".join(sorted(i[8].split("; ")))
        i9 = "; ".join(sorted(i[9].split("; ")))
        miRNA=i[6].split(";")
        n=1
        for j in miRNA:
            j=j.strip().split(":")[0]
            miR_list.append(j)
        miR2="; ".join(sorted(miR_list))
        miR_tuple=(i[0],i[1],i[2],i[3],i[4],i[5],miR2,i[7],i8,i9)
        data.append(miR_tuple)
        n+=1
    data=sorted(data,key=lambda x: x[3])
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    pagination = Pagination(page=page, per_page=per_page, total=len(genes), css_framework='bootstrap3')
    s = (page - 1) * per_page
    e = s + per_page
    numbers = data[s:e]
    sum=len(genes)
    name="TCGA"
    return render_template("TCGA.html", numbers=numbers, name=name,sum=sum,pagination=pagination)

@app.route("/CCLE")
def CCLE():
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Thyroid,Salivary_gland,Soft_tissue,Haematopoietic_and_lymphoid_tissue,Biliary_tract,Pancreas,Central_nervous_system,Small_intestine,Bone,Large_intestine,Autonomic_ganglia,Pleura,Urinary_tract,Lung,Breast,Skin,Ovary,Prostate,Kidney,Upper_aerodigestive_tract,Stomach,Endometrium,Oesophagus,Liver FROM CCLE'''
    curs.execute(sql_count)
    result = curs.fetchall()
    # print result
    genes = list(result)
    data = []
    
    for i in genes:
        miR_list = []
        i6 = "; ".join(sorted(i[6].split("; ")))
        i7 = "; ".join(sorted(i[7].split("; ")))
        miRNA = i[4].split(";")
        
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        miR2 = "; ".join(sorted(miR_list))
        miR_tuple = (i[0], i[1], i[2], i[3],miR2,i[5:],i6,i7)
        data.append(miR_tuple)
    data = sorted(data, key=lambda x: x[1])
    
    data2=[]
    n=1
    for j in data:
        j=j+(str(n),)
        data2.append(tuple(j))
        n=n+1
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    pagination = Pagination(page=page, per_page=per_page, total=len(genes), css_framework='bootstrap3')
    s = (page - 1) * per_page
    e = s + per_page
    numbers = data2[s:e]
    sum=len(genes)
    name="CCLE"
    return render_template("CCLE.html", name=name, numbers=numbers, sum=sum,pagination=pagination)

@app.route("/GTEx")
def GTEx():
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Artery,Bladder,Brain,Breast,Transformed_fibroblasts,Cervix,Colon,Esophagus,Fallopian_tube,Heart,Kidney,Liver,Lung,Salivary_gland,Muscle,Tibial_nerve,Ovary,Pancreas,Pituitary,Prostate,Skin,Small_intestine,Spleen,Stomach,Testis,Thyroid,Uterus,Vagina,Blood FROM GTEx'''
    curs.execute(sql_count)
    result = curs.fetchall()
    # print result
    genes = list(result)
    data = []
    for i in genes:
        miR_list = []
        i6 = "; ".join(sorted(i[6].split("; ")))
        i7 = "; ".join(sorted(i[7].split("; ")))
        miRNA = i[4].split(";")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        miR2 = "; ".join(sorted(miR_list))
        miR_tuple = (i[0], i[1], i[2], i[3], miR2,i[5],i6,i7)
        data.append(miR_tuple)
    data = sorted(data, key=lambda x: x[1])
    data2=[]
    n=1
    for j in data:
        j=j+(str(n),)
        data2.append(tuple(j))
        n=n+1
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    pagination = Pagination(page=page, per_page=per_page, total=len(genes), css_framework='bootstrap3')
    s = (page - 1) * per_page
    e = s + per_page
    numbers = data2[s:e]
    sum=len(genes)
    name="GTEx"
    return render_template("GTEx.html", name=name, numbers=numbers, sum=sum,pagination=pagination)

@app.route("/BodyMap")
def BodyMap():
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Duodenum,Placenta,Lung,Brain,Ovary,Thyroid,Smooth_muscle,Stomach,Endometrium,Heart,Tonsil,Salivary_gland,Breast,Cerebral_cortex,Lymph_node,Spleen,Testis,Skeletal_muscle,Small_intestine,Colon,Liver,Skin,Fallopian_tube,Rectum,Pancreas,Leukocyte,Kidney,Esophagus,Bladder,Bone_marrow,Appendix,Gall_bladder,Prostate FROM EBI'''
    curs.execute(sql_count)
    result = curs.fetchall()
    genes = list(result)
    data = []
    for i in genes:
        miR_list = []
        i6 = "; ".join(sorted(i[6].split("; ")))
        i7 = "; ".join(sorted(i[7].split("; ")))
        miRNA = i[4].split(";")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        miR2 = "; ".join(sorted(miR_list))
        miR_tuple = (i[0], i[1], i[2], i[3], miR2, i[5],i6,i7)
        data.append(miR_tuple)
    data = sorted(data, key=lambda x: x[1])
    data2=[]
    n=1
    for j in data:
        j=j+(str(n),)
        data2.append(tuple(j))
        n=n+1
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    pagination = Pagination(page=page, per_page=per_page, total=len(genes), css_framework='bootstrap3')
    s = (page - 1) * per_page
    e = s + per_page
    numbers = data2[s:e]
    sum=len(genes)
    name="BodyMap"
    return render_template("BodyMap.html", name=name, numbers=numbers, sum=sum,pagination=pagination)
@app.route("/expBarplotTCGA")
def expBarplotTCGA():
    params_cancer = request.args.get('cancer', '')
    input_gene = request.args.get('gene', '')
    input_term=params_cancer+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_TCGA_exp = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA where cancer="%s" and gene="%s"''' % (params_cancer, input_gene)
    curs.execute(sql_TCGA_exp)
    result = curs.fetchall()
    genes = list(result)
    for i in genes:
        # if params_cancer == i[3] and input_gene == i[4]:
        gene=i[4]
        cancer_name=["BLCA","HNSC","THCA","PRAD","ACC","KICH","UVM","THYM","MESO","CHOL","STES","OV","UCEC","LUAD","COAD","BRCA","DLBC","KIRC","STAD","LGG","READ","ESCA","LAML","LIHC","GBM","KIRP","PCPG","UCS","LUSC","TGCT","SARC","SKCM","CESC","PAAD"]
        exp=i[10:]
        dic=dict(zip(cancer_name,exp))
        cap = '<chart caption="Expression level of gene '+gene+' in different cancers"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Cancer name"  palette="1" numdivlines="3" theme="ocean">'
        # cap = '<chart caption = "Monthly Revenue" subcaption = "Last year" xaxisname = "Month" yaxisname = "Amount (In USD)" placevaluesinside = "1" rotatevalues = "1" valuefontcolor = "#ffffff" canvasbgcolor = "#1790e1" canvasbgalpha = "10" canvasborderthickness = "1" showalternatehgridcolor = "0" bgcolor = "#eeeeee" theme = "fint" ><categories>'
        a = sorted(dic.keys())
        seg = []
        for k in a:
            rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
            seg.append(rlt)
        renderdata = cap + ''.join(seg) + "</chart>"
        # print renderdata
        return render_template("cancerExp.html", render_data=renderdata)
@app.route("/expBarplotCCLE")
def expBarplotCCLE():
    params_tissue = request.args.get('tissue', '')
    params_tissue = params_tissue.encode('gb2312')
    # print params_tissue
    input_gene = request.args.get('gene', '')
    input_term=params_tissue+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    # print input_gene
    curs = mysql.connection.cursor()
    sql_CCLE_exp = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Thyroid,Salivary_gland,Soft_tissue,Haematopoietic_and_lymphoid_tissue,Biliary_tract,Pancreas,Central_nervous_system,Small_intestine,Bone,Large_intestine,Autonomic_ganglia,Pleura,Urinary_tract,Lung,Breast,Skin,Ovary,Prostate,Kidney,Upper_aerodigestive_tract,Stomach,Endometrium,Oesophagus,Liver FROM CCLE where tissue="%s" and gene="%s"''' % (params_tissue, input_gene)
    # sql_TCGA_exp = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA'''
    curs.execute(sql_CCLE_exp)
    result = curs.fetchall()
    genes = list(result)
    for i in genes:
        # if params_tissue == i[1] and input_gene == i[2]:
            # print i
        gene=i[2]
        tissue_name=["Thyroid","Salivary gland","Soft tissue","Haematopoietic and lymphoid tissue","Biliary tract","Pancreas","Central nervous system","Small intestine","Bone","Large intestine","Autonomic ganglia","Pleura","Urinary tract","Lung","Breast","Skin","Ovary","Prostate","Kidney","Upper aerodigestive tract","Stomach","Endometrium","Oesophagus","Liver"]
        exp=i[8:]
        dic=dict(zip(tissue_name,exp))
        cap = '<chart caption="Expression level of gene '+gene+' in different tissues"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Tissue name"  palette="1" numdivlines="3" theme="ocean">'
        # cap = '<chart caption = "Monthly Revenue" subcaption = "Last year" xaxisname = "Month" yaxisname = "Amount (In USD)" placevaluesinside = "1" rotatevalues = "1" valuefontcolor = "#ffffff" canvasbgcolor = "#1790e1" canvasbgalpha = "10" canvasborderthickness = "1" showalternatehgridcolor = "0" bgcolor = "#eeeeee" theme = "fint" ><categories>'
        a = sorted(dic.keys())
        seg = []
        for k in a:
            rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
            seg.append(rlt)
        renderdata = cap + ''.join(seg) + "</chart>"
        # print renderdata
        return render_template("cancerExp.html", render_data=renderdata)

@app.route("/expBarplotBodyMap")
def expBarplotBodyMap():
    params_tissue = request.args.get('tissue', '')
    params_tissue = params_tissue.encode('gb2312')
    # print params_tissue
    input_gene = request.args.get('gene', '')
    input_term=params_tissue+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    # print input_gene
    curs = mysql.connection.cursor()
    sql_BodyMap_exp = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Duodenum,Placenta,Lung,Brain,Ovary,Thyroid,Smooth_muscle,Stomach,Endometrium,Heart,Tonsil,Salivary_gland,Breast,Cerebral_cortex,Lymph_node,Spleen,Testis,Skeletal_muscle,Small_intestine,Colon,Liver,Skin,Fallopian_tube,Rectum,Pancreas,Leukocyte,Kidney,Esophagus,Bladder,Bone_marrow,Appendix,Gall_bladder,Prostate FROM EBI where tissue="%s" and gene="%s"''' % (params_tissue, input_gene)
    curs.execute(sql_BodyMap_exp)
    result = curs.fetchall()
    genes = list(result)
    for i in genes:
        # if params_tissue == i[1] and input_gene == i[2]:
        gene=i[2]
        tissue_name=["Adipose","Adrenal gland","Duodenum","Placenta","Lung","Brain","Ovary","Thyroid","Smooth muscle","Stomach","Endometrium","Heart","Tonsil","Salivary gland","Breast","Cerebral cortex","Lymph node","Spleen","Testis","Skeletal muscle","Small intestine","Colon","Liver","Skin","Fallopian tube","Rectum","Pancreas","Leukocyte","Kidney","Esophagus","Bladder","Bone marrow","Appendix","Gall bladder","Prostate"]
        exp=i[8:]
        dic=dict(zip(tissue_name,exp))
        cap = '<chart caption="Expression level of gene '+gene+' in different tissues"' + ' yaxisname="RPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Tissue name"  palette="1" numdivlines="3" theme="ocean">'
        # cap = '<chart caption = "Monthly Revenue" subcaption = "Last year" xaxisname = "Month" yaxisname = "Amount (In USD)" placevaluesinside = "1" rotatevalues = "1" valuefontcolor = "#ffffff" canvasbgcolor = "#1790e1" canvasbgalpha = "10" canvasborderthickness = "1" showalternatehgridcolor = "0" bgcolor = "#eeeeee" theme = "fint" ><categories>'
        a = sorted(dic.keys())
        seg = []
        for k in a:
            rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
            seg.append(rlt)
        renderdata = cap + ''.join(seg) + "</chart>"
        # print renderdata
        return render_template("cancerExp.html", render_data=renderdata)

@app.route("/expBarplotGTEx")
def expBarplotGTEx():
    params_tissue = request.args.get('tissue', '')
    params_tissue = params_tissue.encode('gb2312')
    input_gene = request.args.get('gene', '')
    input_term=params_tissue+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_GTEx_exp = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Artery,Bladder,Brain,Breast,Transformed_fibroblasts,Cervix,Colon,Esophagus,Fallopian_tube,Heart,Kidney,Liver,Lung,Salivary_gland,Muscle,Tibial_nerve,Ovary,Pancreas,Pituitary,Prostate,Skin,Small_intestine,Spleen,Stomach,Testis,Thyroid,Uterus,Vagina,Blood FROM GTEx where tissue="%s" and gene="%s"''' % (params_tissue, input_gene)
    curs.execute(sql_GTEx_exp)
    result = curs.fetchall()
    genes = list(result)
    for i in genes:
        # if params_tissue == i[1] and input_gene == i[2]:
        gene=i[2]
        tissue_name=["Adipose tissue","Adrenal gland","Artery","Bladder","Brain","Breast","Transformed fibroblasts","Cervix","Colon","Esophagus","Fallopian tube","Heart","Kidney","Liver","Lung","Salivary gland","Muscle","Tibial nerve","Ovary","Pancreas","Pituitary","Prostate","Skin","Small intestine","Spleen","Stomach","Testis","Thyroid","Uterus","Vagina","Blood"]
        exp=i[8:]
        dic=dict(zip(tissue_name,exp))
        cap = '<chart caption="Expression level of gene '+gene+' in different tissues"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Tissue name"  palette="1" numdivlines="3" theme="ocean">'
        a = sorted(dic.keys())
        seg = []
        for k in a:
            rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
            seg.append(rlt)
        renderdata = cap + ''.join(seg) + "</chart>"
        # print renderdata
        return render_template("cancerExp.html", render_data=renderdata)


@app.route("/expBarplotSearchAll")
def expBarplotSearchAll():
    params_source = request.args.get('source', '')
    params_tissue = request.args.get('tissue', '')
    params_tissue = params_tissue.encode('gb2312')
    input_gene = request.args.get('gene', '')
    input_term=params_source+params_tissue+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA where cancer="%s" and gene="%s"''' % (params_tissue, input_gene)
    sql_count_BodyMap = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Duodenum,Placenta,Lung,Brain,Ovary,Thyroid,Smooth_muscle,Stomach,Endometrium,Heart,Tonsil,Salivary_gland,Breast,Cerebral_cortex,Lymph_node,Spleen,Testis,Skeletal_muscle,Small_intestine,Colon,Liver,Skin,Fallopian_tube,Rectum,Pancreas,Leukocyte,Kidney,Esophagus,Bladder,Bone_marrow,Appendix,Gall_bladder,Prostate FROM EBI where tissue="%s" and gene="%s"''' % (params_tissue, input_gene)
    sql_count_CCLE = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Thyroid,Salivary_gland,Soft_tissue,Haematopoietic_and_lymphoid_tissue,Biliary_tract,Pancreas,Central_nervous_system,Small_intestine,Bone,Large_intestine,Autonomic_ganglia,Pleura,Urinary_tract,Lung,Breast,Skin,Ovary,Prostate,Kidney,Upper_aerodigestive_tract,Stomach,Endometrium,Oesophagus,Liver FROM CCLE where tissue="%s" and gene="%s"''' % (params_tissue, input_gene)
    sql_count_GTEx = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Artery,Bladder,Brain,Breast,Transformed_fibroblasts,Cervix,Colon,Esophagus,Fallopian_tube,Heart,Kidney,Liver,Lung,Salivary_gland,Muscle,Tibial_nerve,Ovary,Pancreas,Pituitary,Prostate,Skin,Small_intestine,Spleen,Stomach,Testis,Thyroid,Uterus,Vagina,Blood FROM GTEx where tissue="%s" and gene="%s"''' % (params_tissue, input_gene)
    curs.execute(sql_count_TCGA)
    result_TCGA = curs.fetchall()
    curs.execute(sql_count_BodyMap)
    result_BodyMap = curs.fetchall()
    curs.execute(sql_count_CCLE)
    result_CCLE = curs.fetchall()
    curs.execute(sql_count_GTEx)
    result_GTEx = curs.fetchall()
    genes_TCGA = list(result_TCGA)
    genes_BodyMap = list(result_BodyMap)
    genes_CCLE = list(result_CCLE)
    genes_GTEx = list(result_GTEx)
    if params_source == "TCGA":
        for i in genes_TCGA:
            if params_tissue == i[3] and input_gene == i[4]:
                gene=i[4]
                cancer_name=["BLCA","HNSC","THCA","PRAD","ACC","KICH","UVM","THYM","MESO","CHOL","STES","OV","UCEC","LUAD","COAD","BRCA","DLBC","KIRC","STAD","LGG","READ","ESCA","LAML","LIHC","GBM","KIRP","PCPG","UCS","LUSC","TGCT","SARC","SKCM","CESC","PAAD"]
                exp=i[10:]
                dic=dict(zip(cancer_name,exp))
                cap = '<chart caption="Expression level of gene '+gene+' in different cancers"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Cancer name"  palette="1" numdivlines="3" theme="ocean">'
                # cap = '<chart caption = "Monthly Revenue" subcaption = "Last year" xaxisname = "Month" yaxisname = "Amount (In USD)" placevaluesinside = "1" rotatevalues = "1" valuefontcolor = "#ffffff" canvasbgcolor = "#1790e1" canvasbgalpha = "10" canvasborderthickness = "1" showalternatehgridcolor = "0" bgcolor = "#eeeeee" theme = "fint" ><categories>'
                a = sorted(dic.keys())
                seg = []
                for k in a:
                    rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
                    seg.append(rlt)
                renderdata = cap + ''.join(seg) + "</chart>"
                print renderdata
                return render_template("cancerExp.html", render_data=renderdata)
    if params_source == "CCLE":
        for i in genes_CCLE:
            if params_tissue == i[1] and input_gene == i[2]:
                # print i
                gene = i[2]
                tissue_name = ["Thyroid", "Salivary gland", "Soft tissue", "Haematopoietic and lymphoid tissue",
                               "Biliary tract", "Pancreas", "Central nervous system", "Small intestine", "Bone",
                               "Large intestine", "Autonomic ganglia", "Pleura", "Urinary tract", "Lung", "Breast",
                               "Skin", "Ovary", "Prostate", "Kidney", "Upper aerodigestive tract", "Stomach",
                               "Endometrium", "Oesophagus", "Liver"]
                exp = i[8:]
                dic = dict(zip(tissue_name, exp))
                cap = '<chart caption="Expression level of gene ' + gene + ' in different cancers"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Tissue name"  palette="1" numdivlines="3" theme="ocean">'
                # cap = '<chart caption = "Monthly Revenue" subcaption = "Last year" xaxisname = "Month" yaxisname = "Amount (In USD)" placevaluesinside = "1" rotatevalues = "1" valuefontcolor = "#ffffff" canvasbgcolor = "#1790e1" canvasbgalpha = "10" canvasborderthickness = "1" showalternatehgridcolor = "0" bgcolor = "#eeeeee" theme = "fint" ><categories>'
                a = sorted(dic.keys())
                seg = []
                for k in a:
                    rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
                    seg.append(rlt)
                renderdata = cap + ''.join(seg) + "</chart>"
                # print renderdata
                return render_template("cancerExp.html", render_data=renderdata)
    if params_source == "BodyMap":
        for i in genes_BodyMap:
            if params_tissue == i[1] and input_gene == i[2]:
                gene = i[2]
                tissue_name = ["Adipose", "Adrenal gland", "Duodenum", "Placenta", "Lung", "Brain", "Ovary", "Thyroid",
                               "Smooth muscle", "Stomach", "Endometrium", "Heart", "Tonsil", "Salivary gland", "Breast",
                               "Cerebral cortex", "Lymph node", "Spleen", "Testis", "Skeletal muscle",
                               "Small intestine", "Colon", "Liver", "Skin", "Fallopian tube", "Rectum", "Pancreas",
                               "Leukocyte", "Kidney", "Esophagus", "Bladder", "Bone marrow", "Appendix", "Gall bladder",
                               "Prostate"]
                exp = i[8:]
                dic = dict(zip(tissue_name, exp))
                cap = '<chart caption="Expression level of gene ' + gene + ' in different cancers"' + ' yaxisname="RPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Tissue name"  palette="1" numdivlines="3" theme="ocean">'
                # cap = '<chart caption = "Monthly Revenue" subcaption = "Last year" xaxisname = "Month" yaxisname = "Amount (In USD)" placevaluesinside = "1" rotatevalues = "1" valuefontcolor = "#ffffff" canvasbgcolor = "#1790e1" canvasbgalpha = "10" canvasborderthickness = "1" showalternatehgridcolor = "0" bgcolor = "#eeeeee" theme = "fint" ><categories>'
                a = sorted(dic.keys())
                seg = []
                for k in a:
                    rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
                    seg.append(rlt)
                renderdata = cap + ''.join(seg) + "</chart>"
                # print renderdata
                return render_template("cancerExp.html", render_data=renderdata)
    if params_source == "GTEx":
        for i in genes_GTEx:
            if params_tissue == i[1] and input_gene == i[2]:
                gene = i[2]
                tissue_name = ["Adipose tissue", "Adrenal gland", "Artery", "Bladder", "Brain", "Breast",
                               "Transformed fibroblasts", "Cervix", "Colon", "Esophagus", "Fallopian tube", "Heart",
                               "Kidney", "Liver", "Lung", "Salivary gland", "Muscle", "Tibial nerve", "Ovary",
                               "Pancreas", "Pituitary", "Prostate", "Skin", "Small intestine", "Spleen", "Stomach",
                               "Testis", "Thyroid", "Uterus", "Vagina", "Blood"]
                exp = i[8:]
                dic = dict(zip(tissue_name, exp))
                cap = '<chart caption="Expression level of gene ' + gene + ' in different cancers"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Tissue name"  palette="1" numdivlines="3" theme="ocean">'
                # cap = '<chart caption = "Monthly Revenue" subcaption = "Last year" xaxisname = "Month" yaxisname = "Amount (In USD)" placevaluesinside = "1" rotatevalues = "1" valuefontcolor = "#ffffff" canvasbgcolor = "#1790e1" canvasbgalpha = "10" canvasborderthickness = "1" showalternatehgridcolor = "0" bgcolor = "#eeeeee" theme = "fint" ><categories>'
                a = sorted(dic.keys())
                seg = []
                for k in a:
                    rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
                    seg.append(rlt)
                renderdata = cap + ''.join(seg) + "</chart>"
                # print renderdata
                return render_template("cancerExp.html", render_data=renderdata)

@app.route("/TCGAtables")
def TCGAtables():
    params1 = request.args.get('cancer', '')
    params2 = request.args.get('tag', '')
    input_term=params1+params2
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA where cancer="%s" and tag="%s"''' % (params1,params2)
    # sql_count = '''SELECT id, cancer,gene,tag,miR,gene_TF,TF_target, cancer_full_name,tissue,met_number FROM TCGA'''
    curs.execute(sql_count)
    result = curs.fetchall()
    # print result
    genes = list(result)
    # print genes
    data0=[]
    for i in genes:
        miR_list = []
        miRNA = i[6].split(";")
        i8 = "; ".join(sorted(i[8].split("; ")))
        i9 = "; ".join(sorted(i[9].split("; ")))
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        miR = "; ".join(miR_list)
        miR_tuple = (i[0], i[1], i[2], i[3], i[4], i[5], miR,i[7],i8,i9)
        data0.append(miR_tuple)
    data=sorted(data0, key=lambda x: x[4])
    # print data
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 200))
    pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap3')
    s = (page - 1) * per_page
    e = s + per_page
    numbers = data[s:e]
    sum=len(data)
    name="TCGA cancer SEG"
    return render_template("TCGA_each_tissue.html", name=name,numbers=numbers, sum=sum,pagination=pagination)
@app.route("/BodyMaptables")
def BodyMaptables():
    params1 = request.args.get('tissue', '')
    params1 = params1.encode('gb2312')
    params2 = request.args.get('tag', '')
    input_term=params1+params2
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    # params2 = params1.encode('gb2312')
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Duodenum,Placenta,Lung,Brain,Ovary,Thyroid,Smooth_muscle,Stomach,Endometrium,Heart,Tonsil,Salivary_gland,Breast,Cerebral_cortex,Lymph_node,Spleen,Testis,Skeletal_muscle,Small_intestine,Colon,Liver,Skin,Fallopian_tube,Rectum,Pancreas,Leukocyte,Kidney,Esophagus,Bladder,Bone_marrow,Appendix,Gall_bladder,Prostate FROM EBI where tissue="%s" and tag="%s"''' % (params1,params2)
    curs.execute(sql_count)
    result = curs.fetchall()
    genes = list(result)
    data0=[]
    for i in genes:
        miR_list = []
        miRNA = i[4].split(";")
        i6="; ".join(sorted(i[6].split("; ")))
        i7="; ".join(sorted(i[7].split("; ")))
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        miR = "; ".join(sorted(miR_list))
        miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6, i7)
        data0.append(miR_tuple)
    data=sorted(data0, key=lambda x: x[2])
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 200))
    pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap3')
    s = (page - 1) * per_page
    e = s + per_page
    numbers = data[s:e]
    sum=len(data)
    name="BodyMap tissue SEG"
    return render_template("BodyMap_each_tissue.html", name=name,numbers=numbers, sum=sum,pagination=pagination)

@app.route("/CCLEtables")
def CCLEtables():
    params1 = request.args.get('tissue', '')
    params1 = params1.encode('gb2312')
    params2 = request.args.get('tag', '')
    input_term=params1+params2
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    # params2 = params2.encode('gb2312')
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Thyroid,Salivary_gland,Soft_tissue,Haematopoietic_and_lymphoid_tissue,Biliary_tract,Pancreas,Central_nervous_system,Small_intestine,Bone,Large_intestine,Autonomic_ganglia,Pleura,Urinary_tract,Lung,Breast,Skin,Ovary,Prostate,Kidney,Upper_aerodigestive_tract,Stomach,Endometrium,Oesophagus,Liver FROM CCLE where tissue="%s" and tag="%s"''' % (params1,params2)
    curs.execute(sql_count)
    result = curs.fetchall()
    genes = list(result)
    data0 = []
    for i in genes:
        # if line[1] == params1 and line[3] == params2:
            # seg.append(line)
        miR_list = []
        miRNA = i[4].split("; ")
        i6 = "; ".join(sorted(i[6].split("; ")))
        i7 = "; ".join(sorted(i[7].split("; ")))
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        miR = "; ".join(sorted(miR_list))
        miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5], i6, i7)
        data0.append(miR_tuple)
    data=sorted(data0, key=lambda x: x[2])
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 200))
    pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap3')
    s = (page - 1) * per_page
    e = s + per_page
    numbers = data[s:e]
    sum = len(data)
    name = "CCLE tissue SEG"
    return render_template("CCLE_each_tissue.html", name=name,numbers=numbers, sum=sum, pagination=pagination)

@app.route("/GTExtables")
def GTExtables():
    params1 = request.args.get('tissue', '')
    params1 = params1.encode('gb2312')
    params2 = request.args.get('tag', '')
    input_term=params1+params2
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    # print params1
    # params2 = params2.encode('gb2312')
    curs = mysql.connection.cursor()
    sql_count = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Artery,Bladder,Brain,Breast,Transformed_fibroblasts,Cervix,Colon,Esophagus,Fallopian_tube,Heart,Kidney,Liver,Lung,Salivary_gland,Muscle,Tibial_nerve,Ovary,Pancreas,Pituitary,Prostate,Skin,Small_intestine,Spleen,Stomach,Testis,Thyroid,Uterus,Vagina,Blood FROM GTEx where tissue="%s" and tag="%s"''' % (params1,params2)
    curs.execute(sql_count)
    result = curs.fetchall()
    genes = list(result)
    # seg=[]
    data0 = []
    for i in genes:
        miR_list = []
        miRNA = i[4].split("; ")
        i6 = "; ".join(sorted(i[6].split("; ")))
        i7 = "; ".join(sorted(i[7].split("; ")))
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        miR = "; ".join(sorted(miR_list))
        miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5], i6, i7)
        data0.append(miR_tuple)
    data=sorted(data0, key=lambda x: x[2])
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 200))
    pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap3')
    s = (page - 1) * per_page
    e = s + per_page
    numbers = data[s:e]
    sum=len(data)
    name = "GTEx tissue SEG"
    return render_template("GTEx_each_tissue.html", name=name,numbers=numbers, sum=sum,pagination=pagination)
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/TCGAnetwork")
def TCGAnetwork():
    # cname='TCGA'
    tname = "TCGA"
    tissuename = "cancer"
    params_cancer = request.args.get('cancer', '')
    params_cancer = params_cancer.encode('gb2312')
    input_gene = request.args.get('gene', '')
    input_term=params_cancer+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id, cancer,gene,tag,miR,gene_TF,TF_target FROM TCGA'''
    curs.execute(sql_count_TCGA)
    result = curs.fetchall()
    genes = list(result)
    params_miR=[]
    input_gene_TF=[]
    params_TF_gene=[]
    for i in genes:
        miR_list = []
        miRNA = i[4].split("; ")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        if params_cancer==i[1] and input_gene==i[2]:
            params_miR.extend(miR_list)
            input_gene_TF.extend(i[5].split('; '))
            params_TF_gene.extend(i[6].split('; '))
    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        m = 1000
        o = 10000
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        for i in params_TF_gene:
            i = i.strip()
            node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
            edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
            attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
            seg_node.append(node4)
            seg_edge.append(edge4)
            seg_attr.append(attr4)
            o += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        o = 10000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        for i in params_TF_gene:
            i = i.strip()
            node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
            edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
            attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
            seg_node.append(node4)
            seg_edge.append(edge4)
            seg_attr.append(attr4)
            o += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1='\\<node id = "-1"><data key = "label">'+input_gene+'</data></node>'
        seg_node.append(node1)
        n=0
        m = 1000
        for j in params_miR:
            j=j.strip()
            node2='\\<node id="'+str(n)+'"><data key="label">'+j+'</data></node>'
            edge2 = '\\<edge source="'+str(n)+'" target="-1"></edge>'
            attr2='{ attrValue: '+str(n)+', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n+=1
        for i in input_gene_TF:
            i=i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m+=1
        seg_edge.append('\\           </graph>'+'\\'+'\n'+'</graphml>\\')
        totaldata=''.join(seg_node)+''.join(seg_edge)
        totalattr=''.join(seg_attr)
        # print totaldata
        # print totalattr
        return render_template("allDBnetwork.html",total_data=totaldata,total_attr=totalattr,tname=tname,tissuename=tissuename,cancername=str(params_cancer),genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        # print totaldata
        # print totalattr
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr,tname=tname,tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        # print totaldata
        # print totalattr
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr,tname=tname,tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_miR:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        # print totaldata
        # print totalattr
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        return render_template("allDBnetwork.html", total_data='', total_attr='',tname=tname,tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))

@app.route("/miRNATFgene",methods=['GET','POST'])
def miRNATFgene():
    data_source=request.form.get("source")
    input_tissue0 = request.form.get("tissue").encode('gb2312')
    if data_source=="TCGA":
        input_tissue = input_tissue0.split("(")[0].strip()
    if data_source=="CCLE" or data_source=="BodyMap" or data_source=="GTEx":
        input_tissue = input_tissue0
    input_miRNA1 = request.form.get("miRNA1",'')
    input_miRNA2 = request.form.get("miRNA2",'')
    input_TF1 = request.form.get("TF1",'')
    input_TF2 = request.form.get("TF2",'')
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    total_list=list(input_miRNA1)+list(input_miRNA2)+list(input_TF1)+list(input_TF2)
    flag=0
    for i in set(total_list):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Invalid character input !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html", code=code)
            flag=1
            break
    if flag==0:
        return render_template("miRNATFgene.html", source=data_source,tissue=input_tissue,miRNA1=input_miRNA1,miRNA2=input_miRNA2, TF1=input_TF1,TF2=input_TF2)
@app.route("/datajson")
def datajson():
    dataSource=request.args.get("source")
    tissue = request.args.get("tissue").encode('gb2312')
    miRNA1 = request.args.get("miRNA1")
    miRNA1=miRNA1.encode('gb2312')
    miRNA2 = request.args.get("miRNA2")
    miRNA2 = miRNA2.encode('gb2312')
    TF1 = request.args.get("TF1",'')
    TF1=TF1.encode('gb2312')
    TF2 = request.args.get("TF2",'')
    TF2 = TF2.encode('gb2312')
    input_term=dataSource+tissue+miRNA1+miRNA2+TF1+TF2
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    if dataSource == "TCGA":
        sql = '''SELECT id,cancer,gene,tag,miR,gene_TF,TF_target FROM TCGA where cancer="%s" ''' % (tissue)
    if dataSource == "BodyMap":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM EBI where tissue="%s" ''' % (tissue)
    if dataSource == "CCLE":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM CCLE where tissue="%s" ''' % (tissue)
    if dataSource == "GTEx":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM GTEx where tissue="%s" ''' % (tissue)
    curs.execute(sql)
    result = curs.fetchall()
    genes = list(result)
    # print genes
    miR_dic={}
    TF_dic={}
    for i in genes:
        id, cancer, gene, tag, miR, gene_TF, TF_target = i
        miRNA = miR.split("; ")
        TF = gene_TF.split("; ")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_dic.setdefault(j, []).append(gene)
        for jj in TF:
            jj=jj.strip()
            TF_dic.setdefault(jj, []).append(gene)
    node_list=[]
    edge_list=[]
    result_json = []
    node_miR=[]
    node_TF=[]
    if miRNA1 in miR_dic and miRNA2 in miR_dic and TF1 not in TF_dic and TF2 not in TF_dic:
        miRNA1_target=miR_dic[miRNA1]
        miRNA2_target=miR_dic[miRNA2]
        colist=list(set(miRNA1_target).intersection(set(miRNA2_target)))
        if colist:
            node_list.append(miRNA1)
            node_list.append(miRNA2)
            node_list.extend(colist)
            node_miR.append(miRNA1)
            node_miR.append(miRNA2)
            for target in colist:
                edge_list.append((miRNA1,target))
                edge_list.append((miRNA2, target))
    if miRNA1 not in miR_dic and miRNA2 in miR_dic and TF1 not in TF_dic and TF2 in TF_dic:
        miRNA2_target=miR_dic[miRNA2]
        TF2_target = TF_dic[TF2]
        colist=list(set(miRNA2_target).intersection(set(TF2_target)))
        if colist:
            node_list.append(miRNA2)
            node_list.append(TF2)
            node_list.extend(colist)
            node_miR.append(miRNA2)
            node_miR.append(TF2)
            for target in colist:
                edge_list.append((miRNA2,target))
                edge_list.append((TF2, target))
    if miRNA1 not in miR_dic and miRNA2 in miR_dic and TF1 in TF_dic and TF2 not in TF_dic:
        miRNA2_target=miR_dic[miRNA2]
        TF1_target = TF_dic[TF1]
        colist=list(set(miRNA2_target).intersection(set(TF1_target)))
        if colist:
            node_list.append(miRNA2)
            node_list.append(TF1)
            node_list.extend(colist)
            node_miR.append(miRNA2)
            node_miR.append(TF1)
            for target in colist:
                edge_list.append((miRNA2,target))
                edge_list.append((TF1, target))
    if miRNA1 in miR_dic and miRNA2 not in miR_dic and TF1 not in TF_dic and TF2 in TF_dic:
        miRNA1_target=miR_dic[miRNA1]
        TF2_target = TF_dic[TF2]
        colist=list(set(miRNA1_target).intersection(set(TF2_target)))
        if colist:
            node_list.append(miRNA1)
            node_list.append(TF2)
            node_list.extend(colist)
            node_miR.append(miRNA1)
            node_miR.append(TF2)
            for target in colist:
                edge_list.append((miRNA1,target))
                edge_list.append((TF2, target))
    if miRNA1 not in miR_dic and miRNA2 not in miR_dic and TF1 in TF_dic and TF2 in TF_dic:
        TF1_target = TF_dic[TF1]
        TF2_target = TF_dic[TF2]
        colist = list(set(TF1_target).intersection(set(TF2_target)))
        if colist:
            node_list.append(TF1)
            node_list.append(TF2)
            node_list.extend(colist)
            node_TF.append(TF1)
            node_TF.append(TF2)
            for target in colist:
                edge_list.append((TF1, target))
                edge_list.append((TF2, target))

    if miRNA1 in miR_dic and miRNA2 not in miR_dic and TF1 in TF_dic and TF2 not in TF_dic:
        miRNA1_target = miR_dic[miRNA1]
        TF1_target = TF_dic[TF1]
        colist = list(set(miRNA1_target).intersection(set(TF1_target)))
        if colist:
            node_list.append(miRNA1)
            node_list.append(TF1)
            node_list.extend(colist)
            node_miR.append(miRNA1)
            node_TF.append(TF1)
            for target in colist:
                edge_list.append((miRNA1, target))
                edge_list.append((TF1, target))

    if miRNA1 in miR_dic and miRNA2 in miR_dic and TF1 in TF_dic and TF2 not in TF_dic:
        miRNA1_target = miR_dic[miRNA1]
        miRNA2_target = miR_dic[miRNA2]
        TF1_target = TF_dic[TF1]
        colist = list(set(miRNA1_target).intersection(set(miRNA2_target)).intersection(set(TF1_target)))
        if colist:
            node_list.append(miRNA1)
            node_list.append(miRNA2)
            node_list.append(TF1)
            node_list.extend(colist)
            node_miR.append(miRNA1)
            node_miR.append(miRNA2)
            node_TF.append(TF1)
            for target in colist:
                edge_list.append((miRNA1, target))
                edge_list.append((miRNA2, target))
                edge_list.append((TF1, target))

    if miRNA1 in miR_dic and miRNA2 not in miR_dic and TF1 in TF_dic and TF2 in TF_dic:
        miRNA1_target = miR_dic[miRNA1]
        TF1_target = TF_dic[TF1]
        TF2_target = TF_dic[TF2]
        colist = list(set(miRNA1_target).intersection(set(TF2_target)).intersection(set(TF1_target)))
        if colist:
            node_list.append(miRNA1)
            node_list.append(TF1)
            node_list.append(TF2)
            node_list.extend(colist)
            node_miR.append(miRNA1)
            node_TF.append(TF1)
            node_TF.append(TF2)
            for target in colist:
                edge_list.append((miRNA1, target))
                edge_list.append((TF1, target))
                edge_list.append((TF2, target))

    if miRNA1 not in miR_dic and miRNA2 not in miR_dic and TF1 in TF_dic and TF2 not in TF_dic:
        TF1_target = TF_dic[TF1]
        colist = TF1_target
        if colist:
            node_list.append(TF1)
            node_list.extend(colist)
            node_TF.append(TF1)
            for target in colist:
                edge_list.append((TF1, target))
    if miRNA1 not in miR_dic and miRNA2 not in miR_dic and TF1 not in TF_dic and TF2 in TF_dic:
        TF2_target = TF_dic[TF2]
        colist = TF2_target
        if colist:
            node_list.append(TF2)
            node_list.extend(colist)
            node_TF.append(TF2)
            for target in colist:
                edge_list.append((TF2, target))
    if miRNA1 in miR_dic and miRNA2 not in miR_dic and TF1 not in TF_dic and TF2 not in TF_dic:
        miRNA1_target = miR_dic[miRNA1]
        colist = miRNA1_target
        if colist:
            node_list.append(miRNA1)
            node_list.extend(colist)
            node_miR.append(miRNA1)
            for target in colist:
                edge_list.append((miRNA1, target))
    if miRNA1 not in miR_dic and miRNA2 in miR_dic and TF1 not in TF_dic and TF2 not in TF_dic:
        miRNA2_target = miR_dic[miRNA2]
        colist = miRNA2_target
        if colist:
            node_list.append(miRNA2)
            node_list.extend(colist)
            node_miR.append(miRNA2)
            for target in colist:
                edge_list.append((miRNA2, target))

    if miRNA1 in miR_dic and miRNA2 in miR_dic and TF1 in TF_dic and TF2 in TF_dic:
        miRNA1_target = miR_dic[miRNA1]
        miRNA2_target = miR_dic[miRNA2]
        TF1_target = TF_dic[TF1]
        TF2_target = TF_dic[TF2]
        colist = list(set(miRNA1_target).intersection(set(miRNA2_target)).intersection(set(TF2_target)).intersection(set(TF1_target)))
        if colist:
            node_list.append(miRNA1)
            node_list.append(miRNA2)
            node_list.append(TF1)
            node_list.append(TF2)
            node_list.extend(colist)
            node_miR.append(miRNA1)
            node_miR.append(miRNA2)
            node_TF.append(TF1)
            node_TF.append(TF2)
            for target in colist:
                edge_list.append((miRNA1, target))
                edge_list.append((miRNA2, target))
                edge_list.append((TF1, target))
                edge_list.append((TF2, target))
    for node in node_list:
        if node in node_miR:
            result_json.append({
                "data": {"id": node,"color":"#ff2"},
                "group": "nodes",
                "removed": False,
                "selected": False,
                "selectable": True,
                "locked": False,
                "grabbable": True,
                "hideLabelsOnViewport": False,
                "classes": ""})
        if node in node_TF:
            result_json.append({
                "data": {"id": node,"color":"#8DB6CD"},
                "group": "nodes",
                "removed": False,
                "selected": False,
                "selectable": True,
                "locked": False,
                "grabbable": True,
                "hideLabelsOnViewport": False,
                "classes": ""})
        if node not in node_TF and node not in node_miR:
            result_json.append({
                "data": {"id": node, "color": "#9ACD32"},
                "group": "nodes",
                "removed": False,
                "selected": False,
                "selectable": True,
                "locked": False,
                "grabbable": True,
                "hideLabelsOnViewport": False,
                "classes": ""})

    for source, target in edge_list:
        # print source, target
        result_json.append({
            "data": {
                "id": "{}-{}".format(source, target),
                "source": source,
                "target": target
            },
            "group": "edges",
            "removed": False,
            "selected": False,
            "selectable": True,
            "locked": False,
            "grabbable": True,
            "classes": ""
        })
    return jsonify(result_json)

@app.route("/network")
def network():
    params_source = request.args.get('source', '')
    params_cancer = request.args.get('tissue', '')
    input_gene = request.args.get('gene', '')
    input_term=params_source+params_cancer+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id, cancer,gene,tag,miR,gene_TF,TF_target,cancer_full_name,tissue FROM TCGA'''
    sql_count_BodyMap = '''SELECT id,tissue,gene,tag,gene_TF,TF_target,tissue_name FROM EBI'''
    sql_count_CCLE = '''SELECT id,tissue,gene,tag,gene_TF,TF_target,tissue_name FROM CCLE'''
    sql_count_GTEx = '''SELECT id,tissue,gene,tag,gene_TF,TF_target,tissue_name FROM GTEx'''
    curs.execute(sql_count_TCGA)
    result_TCGA = curs.fetchall()
    curs.execute(sql_count_BodyMap)
    result_BodyMap = curs.fetchall()
    curs.execute(sql_count_CCLE)
    result_CCLE = curs.fetchall()
    curs.execute(sql_count_GTEx)
    result_GTEx = curs.fetchall()
    genes_TCGA = list(result_TCGA)
    genes_BodyMap = list(result_BodyMap)
    genes_CCLE = list(result_CCLE)
    genes_GTEx = list(result_GTEx)
    data=[]
    for i in genes_TCGA:
        if i[8]==params_cancer and i[2]==input_gene:
            miR_tuple = ("TCGA",i[0], i[1], i[2], i[3], i[4], i[5],i[6],i[7],i[8])
            data.append(miR_tuple)
    for i in genes_BodyMap:
        if i[6] == params_cancer and i[2] == input_gene:
            miR_tuple = ("BodyMap",i[0], i[1], i[2], i[3], "-", i[4], i[5],"-",i[6])
            data.append(miR_tuple)
    for i in genes_CCLE:
        if i[6] == params_cancer and i[2] == input_gene:
            miR_tuple = ("CCLE",i[0], i[1], i[2], i[3], "-", i[4], i[5],"-",i[6])
            data.append(miR_tuple)
    for i in genes_GTEx:
        if i[6] == params_cancer and i[2] == input_gene:
            miR_tuple = ("GTEx",i[0], i[1], i[2], i[3], "-", i[4], i[5],"-",i[6])
            data.append(miR_tuple)
    params_miR=[]
    input_gene_TF=[]
    params_TF_gene=[]
    # print data
    for i in data:
        miR_list = []
        genes5 = i[5].split(";")
        for j in genes5:
            j = j.split(":")[0]
            miR_list.append(j)
        if params_source==i[0] and params_cancer==i[9] and input_gene==i[3]:
            params_miR.extend(miR_list)
            input_gene_TF.extend(i[6].split(';'))
            params_TF_gene.extend(i[7].split(';'))
    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        tname=i[0]
        tissuename = i[9]
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1='\\<node id = "-1"><data key = "label">'+input_gene+'</data></node>'
        seg_node.append(node1)
        n=0
        m = 1000
        for j in params_miR:
            j=j.strip()
            node2='\\<node id="'+str(n)+'"><data key="label">'+j+'</data></node>'
            edge2 = '\\<edge source="'+str(n)+'" target="-1"></edge>'
            attr2='{ attrValue: '+str(n)+', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n+=1
        for i in input_gene_TF:
            i=i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m+=1
        seg_edge.append('\\           </graph>'+'\\'+'\n'+'</graphml>\\')
        totaldata=''.join(seg_node)+''.join(seg_edge)
        totalattr=''.join(seg_attr)
        return render_template("network.html",total_data=totaldata,total_attr=totalattr,tname=tname,tissuename=tissuename,cancername=str(params_cancer),genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        tname = i[0]
        tissuename = i[9]
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        # print totaldata
        # print totalattr
        return render_template("network.html", total_data=totaldata, total_attr=totalattr,tname=tname,tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        tname = i[0]
        tissuename = i[9]
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        print totaldata
        print totalattr
        return render_template("network.html", total_data=totaldata, total_attr=totalattr,tname=tname,tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        tname = i[0]
        tissuename = i[9]
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        # print totaldata
        # print totalattr
        return render_template("network.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        tname = i[0]
        tissuename = i[9]
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_miR:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        # print totaldata
        # print totalattr
        return render_template("network.html", total_data=totaldata, total_attr=totalattr, tname=tname, tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        tname = i[0]
        tissuename =i[9]
        return render_template("network.html", total_data='', total_attr='',tname=tname,tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))
#add_browseGeneNetwork
@app.route("/browseGeneNetwork")
def browseGeneNetwork():
    dataSource = request.args.get("source")
    input_gene = request.args.get('gene')
    input_tissue = request.args.get('tissue')
    input_tissue = input_tissue.encode('gb2312').split('; ')
    input_term=dataSource+input_gene+';'.join(input_tissue)
    alphas_digit = string.ascii_letters + '_+-.;\\\t ' + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    # print dataSource
    # print input_tissue
    # print input_gene
    total_list = []
    if dataSource == "TCGA":
        for i in input_tissue:
            # print i
            sql = '''SELECT id,cancer,gene,tag,miR,gene_TF,TF_target FROM TCGA WHERE cancer="%s" and gene="%s"''' % (i, input_gene)
            # print sql
            curs.execute(sql)
            result = curs.fetchall()
            da = list(result)

            total_list.append(da)
    if dataSource == "BodyMap":
        for i in input_tissue:
            # print i
            sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM EBI WHERE tissue="%s" and gene="%s"''' % (i, input_gene)
            # print sql
            curs.execute(sql)
            result = curs.fetchall()
            da = list(result)
            total_list.append(da)
    if dataSource == "CCLE":
        for i in input_tissue:
            # print i
            sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM CCLE WHERE tissue="%s" and gene="%s"''' % (i, input_gene)
            # print sql
            curs.execute(sql)
            result = curs.fetchall()
            da = list(result)

            total_list.append(da)
    if dataSource == "GTEx":
        for i in input_tissue:
            # print i
            sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM GTEx WHERE tissue="%s" and gene="%s"''' % (i, input_gene)
            # print sql
            curs.execute(sql)
            result = curs.fetchall()
            da = list(result)

            total_list.append(da)
    tissue = []
    total_list2=[]
    download_network=[]
    for genes in total_list:
        params_miR = []
        input_gene_TF = []
        params_TF_gene = []
        t= genes[0][1]
        tissue.append(genes[0][1])

        # print genes
        for i in genes:
            # tissue.add(i[1])
            input_gene_TF.extend(i[5].split('; '))
            params_TF_gene.extend(i[6].split('; '))
            miRNA = i[4].split("; ")
            for j in miRNA:
                j = j.strip().split(":")[0]
                params_miR.append(j)
        
        for d1 in input_gene_TF:
            if d1=='-':
                continue
            node1= d1+','+input_gene+','+'1'+','+ t
            download_network.append(node1)
        for d2 in params_TF_gene:
            if d2=='-':
                continue
            node2=input_gene+','+d2+','+'2'+','+ t
            download_network.append(node2)
        for d3 in params_miR:
            if d3=='-':
                continue
            node3=d3+','+input_gene+','+'3'+','+ t
            download_network.append(node3)
        if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
            seg_node = []
            seg_edge = []
            seg_attr = []
            seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
            node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
            seg_node.append(node1)
            n = 0
            m = 1000
            o = 10000
            for j in params_miR:
                j = j.strip()
                node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
                edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
                attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
                seg_node.append(node2)
                seg_edge.append(edge2)
                seg_attr.append(attr2)
                n += 1
            for i in input_gene_TF:
                i = i.strip()
                node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
                edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
                attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
                seg_node.append(node3)
                seg_edge.append(edge3)
                seg_attr.append(attr3)
                m += 1
            for i in params_TF_gene:
                i = i.strip()
                node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
                edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
                attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
                seg_node.append(node4)
                seg_edge.append(edge4)
                seg_attr.append(attr4)
                o += 1
            seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
            totaldata = ''.join(seg_node) + ''.join(seg_edge)
            totalattr = ''.join(seg_attr)
        if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
            seg_node = []
            seg_edge = []
            seg_attr = []
            seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
            node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
            seg_node.append(node1)
            m = 1000
            o = 10000
            for i in input_gene_TF:
                i = i.strip()
                node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
                edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
                attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
                seg_node.append(node3)
                seg_edge.append(edge3)
                seg_attr.append(attr3)
                m += 1
            for i in params_TF_gene:
                i = i.strip()
                node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
                edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
                attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
                seg_node.append(node4)
                seg_edge.append(edge4)
                seg_attr.append(attr4)
                o += 1
            seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
            totaldata = ''.join(seg_node) + ''.join(seg_edge)
            totalattr = ''.join(seg_attr)
        if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
            seg_node = []
            seg_edge = []
            seg_attr = []
            seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
            node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
            seg_node.append(node1)
            n = 0
            m = 1000
            for j in params_miR:
                j = j.strip()
                node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
                edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
                attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
                seg_node.append(node2)
                seg_edge.append(edge2)
                seg_attr.append(attr2)
                n += 1
            for i in input_gene_TF:
                i = i.strip()
                node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
                edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
                attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
                seg_node.append(node3)
                seg_edge.append(edge3)
                seg_attr.append(attr3)
                m += 1
            seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
            totaldata = ''.join(seg_node) + ''.join(seg_edge)
            totalattr = ''.join(seg_attr)
        if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
            seg_node = []
            seg_edge = []
            seg_attr = []
            seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
            node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
            seg_node.append(node1)
            m = 1000
            for i in input_gene_TF:
                i = i.strip()
                node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
                edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
                attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
                seg_node.append(node3)
                seg_edge.append(edge3)
                seg_attr.append(attr3)
                m += 1
            seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
            totaldata = ''.join(seg_node) + ''.join(seg_edge)
            totalattr = ''.join(seg_attr)
        if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
            seg_node = []
            seg_edge = []
            seg_attr = []
            seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
            node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
            seg_node.append(node1)
            n = 0
            for j in params_miR:
                j = j.strip()
                node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
                edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
                attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
                seg_node.append(node2)
                seg_edge.append(edge2)
                seg_attr.append(attr2)
                n += 1
            m = 1000
            for i in params_TF_gene:
                i = i.strip()
                node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
                # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
                edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
                attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
                seg_node.append(node3)
                seg_edge.append(edge3)
                seg_attr.append(attr3)
                m += 1
            seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
            totaldata = ''.join(seg_node) + ''.join(seg_edge)
            totalattr = ''.join(seg_attr)
        if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
            seg_node = []
            seg_edge = []
            seg_attr = []
            seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
            node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
            seg_node.append(node1)
            m = 1000
            for i in params_TF_gene:
                i = i.strip()
                node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
                # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
                edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
                attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
                seg_node.append(node3)
                seg_edge.append(edge3)
                seg_attr.append(attr3)
                m += 1
            seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
            totaldata = ''.join(seg_node) + ''.join(seg_edge)
            totalattr = ''.join(seg_attr)
            # return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, genename=str(input_gene),dataSource=str(dataSource), input_tissue=str(input_tissue))
        # total_list2.append((totaldata, totalattr, genename, dataSource, input_tissue))
        if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
            seg_node = []
            seg_edge = []
            seg_attr = []
            seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
            node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
            seg_node.append(node1)
            m = 1000
            for i in params_miR:
                i = i.strip()
                node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
                edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
                attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
                seg_node.append(node3)
                seg_edge.append(edge3)
                seg_attr.append(attr3)
                m += 1
            seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
            totaldata = ''.join(seg_node) + ''.join(seg_edge)
            totalattr = ''.join(seg_attr)
        if params_miR[0] == '-' and input_gene_TF[0] == '-'and params_TF_gene[0] == '-':
            totaldata = ''
            totalattr = ''
        total_list2.append((totaldata, totalattr))
        header='Regulator'+','+'Gene'+','+'Type'+','+'Cancer/Tissue'+'\\n'
        download_data=header+'\\n'.join(download_network)+'\\n'+'Type 1: TF-gene; 2: Gene (is also a TF) - gene; 3: miRNA-gene'
    genename = str(input_gene)
    dataSource = str(dataSource)
    input_tissue = tissue
    seg=[]
    nn=1
    mm=0
    for li in total_list2:
        # print li
        totaldata, totalattr = li
        if totaldata and totalattr:
            code='''<h3>Regulatory network of %s gene in %s %s</h3>
                    <div id="%sa" style="width:1200px;height:800px;"></div>
                    <script type="text/javascript">
                    var xml = '%s
                    ';
                    var visual_style = {
                        nodes: {
                                    borderColor: "#FFFFFF",
                                    borderWidth: 0,
                                    size: 40,
                                    color: {
                                        discreteMapper: {
                                            attrName: "id",
                                            entries: [
                                                { attrValue: -1, value: "#EEEE00" },
                                                %s
                                               ]
                                        }
                                    },
                                    labelHorizontalAnchor: "center",
                                    labelFontSize: 16,
                                    labelFontColor: "#000000",
                                    labelFontWeight: "bold"
                                }
                    }
                var options = { swfPath: "/static/SEGreg/cytoscape/swf/CytoscapeWeb"}
                var vis = new org.cytoscapeweb.Visualization("%sa",options);
                vis.draw({ network: xml, visualStyle: visual_style });
                </script><br/>''' %(genename,dataSource,input_tissue[mm],nn,totaldata,totalattr,nn)
            nn += 1
            mm+=1
            # print code
            seg.append(code)
        else:
            code='''<h3>Regulatory network of %s gene in %s %s </h3>
                    <div id="%sa" style="width:1200px;height:200px;"><h3 align="center" style="color:blue">No regulatory data found.</h3></div>''' % (genename,dataSource,input_tissue[mm],nn)
            nn += 1
            mm += 1
            seg.append(code)
    return render_template("genenetwork.html", genename=genename,download_data=download_data,code='<br/>'.join(seg))

#end_browseGeneNetwork
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
# error.handler 


@app.route("/allDBnetwork")
def allDBnetwork():
    dataSource = request.args.get("source")
    dataSource = dataSource.encode('gb2312')
    input_tissue = request.args.get('tissue')
    input_tissue = input_tissue.encode('gb2312')
    input_gene = request.args.get('gene')
    input_gene = input_gene.encode('gb2312')
    input_term= dataSource+input_tissue+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    if dataSource == "TCGA":
        sql = '''SELECT id,cancer,gene,tag,miR,gene_TF,TF_target FROM TCGA WHERE cancer="%s" and gene="%s"''' % (input_tissue, input_gene)
        # print sql
    if dataSource == "BodyMap":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM EBI WHERE tissue="%s" and gene="%s"''' % (input_tissue, input_gene)
    if dataSource == "CCLE":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM CCLE WHERE tissue="%s" and gene="%s"''' % (input_tissue, input_gene)
    if dataSource == "GTEx":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM GTEx where tissue="%s" and gene="%s"''' % (input_tissue, input_gene)
    curs.execute(sql)
    result = curs.fetchall()
    genes = list(result)
    params_miR = []
    input_gene_TF = []
    params_TF_gene = []
    download_network=[]
    for i in genes:
        input_gene_TF.extend(i[5].split('; '))
        params_TF_gene.extend(i[6].split('; '))
        miRNA = i[4].split("; ")
        for j in miRNA:
            j = j.strip().split(":")[0]
            params_miR.append(j)
        
    for d1 in input_gene_TF:
        if d1=='-':
            continue
        node1= d1+','+input_gene+','+'1'
        download_network.append(node1)
    for d2 in params_TF_gene:
        if d2=='-':
            continue
        node2=input_gene+','+d2+','+'2'
        download_network.append(node2)
    for d3 in params_miR:
        if d3=='-':
            continue
        node3=d3+','+input_gene+','+'3'
        download_network.append(node3)
    header='Regulator'+','+'Gene'+','+'Type'+'\\n'
    download_data=header+'\\n'.join(download_network)+'\\n'+'Type 1: TF-gene; 2: Gene (is also a TF) - gene; 3: miRNA-gene'
    
    # print download_data

    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        m = 1000
        o = 10000
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        for i in params_TF_gene:
            i = i.strip()
            node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
            edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
            attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
            seg_node.append(node4)
            seg_edge.append(edge4)
            seg_attr.append(attr4)
            o += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        # download_data=download_data
        return render_template("allDBnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, genename=str(input_gene),dataSource=str(dataSource), input_tissue=str(input_tissue))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        o = 10000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        for i in params_TF_gene:
            i = i.strip()
            node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
            edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
            attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
            seg_node.append(node4)
            seg_edge.append(edge4)
            seg_attr.append(attr4)
            o += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        # download_data=download_data
        return render_template("allDBnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, genename=str(input_gene),dataSource=str(dataSource), input_tissue=str(input_tissue))

    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        m = 1000
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, genename=str(input_gene), dataSource=str(dataSource), input_tissue=str(input_tissue))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, genename=str(input_gene), dataSource=str(dataSource), input_tissue=str(input_tissue))
    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, genename=str(input_gene),dataSource=str(dataSource), input_tissue=str(input_tissue))
    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, genename=str(input_gene),dataSource=str(dataSource), input_tissue=str(input_tissue))

    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_miR:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, genename=str(input_gene),dataSource=str(dataSource), input_tissue=str(input_tissue))

    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        return render_template("no_data_found.html", total_data='', total_attr='', genename=str(input_gene),dataSource=str(dataSource), input_tissue=str(input_tissue))


@app.route("/BodyMapnetwork")
def BodyMapnetwork():
    tname="BodyMap"
    tissuename="tissue"
    params_cancer = request.args.get('tissue', '')
    params_cancer=params_cancer.encode('gb2312')
    input_gene = request.args.get('gene', '')
    input_term=tname+tissuename+params_cancer+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_BodyMap = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM EBI'''
    curs.execute(sql_count_BodyMap)
    result = curs.fetchall()
    genes = list(result)
    params_miR = []
    input_gene_TF = []
    params_TF_gene = []
    for i in genes:
        miR_list = []
        miRNA = i[4].split("; ")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        if params_cancer == i[1] and input_gene == i[2]:
            params_miR.extend(miR_list)
            input_gene_TF.extend(i[5].split('; '))
            params_TF_gene.extend(i[6].split('; '))
    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        m = 1000
        o = 10000
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        for i in params_TF_gene:
            i = i.strip()
            node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
            edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
            attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
            seg_node.append(node4)
            seg_edge.append(edge4)
            seg_attr.append(attr4)
            o += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        o = 10000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        for i in params_TF_gene:
            i = i.strip()
            node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
            edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
            attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
            seg_node.append(node4)
            seg_edge.append(edge4)
            seg_attr.append(attr4)
            o += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        m = 1000
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_miR:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        return render_template("allDBnetwork.html", total_data='', total_attr='', tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

@app.route("/GTExnetwork")
def GTExnetwork():
    tname="GTEx"
    tissuename = "tissue"
    params_cancer = request.args.get('tissue', '')
    params_cancer = params_cancer.encode('gb2312')
    input_gene = request.args.get('gene', '')
    input_term=tname+tissuename+params_cancer+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_GTEx = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM GTEx'''
    curs.execute(sql_count_GTEx)
    result = curs.fetchall()
    genes = list(result)
    params_miR = []
    input_gene_TF = []
    params_TF_gene = []
    for i in genes:
        miR_list = []
        miRNA = i[4].split("; ")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miR_list.append(j)
        if params_cancer == i[1] and input_gene == i[2]:
            params_miR.extend(miR_list)
            input_gene_TF.extend(i[5].split('; '))
            params_TF_gene.extend(i[6].split('; '))
    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        m = 1000
        o = 10000
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        for i in params_TF_gene:
            i = i.strip()
            node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
            edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
            attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
            seg_node.append(node4)
            seg_edge.append(edge4)
            seg_attr.append(attr4)
            o += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        o = 10000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        for i in params_TF_gene:
            i = i.strip()
            node4 = '\\<node id="' + str(o) + '"><data key="label">' + i + '</data></node>'
            edge4 = '\\<edge source="-1" ' + 'target="' + str(o) + '"></edge>'
            attr4 = '{ attrValue: ' + str(o) + ', value: "#9ACD32" },'
            seg_node.append(node4)
            seg_edge.append(edge4)
            seg_attr.append(attr4)
            o += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] != '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        m = 1000
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in input_gene_TF:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        n = 0
        for j in params_miR:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="' + str(n) + '" target="-1"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))
    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m) + '"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] != '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_miR:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr, tname=tname,tissuename=tissuename, cancername=str(params_cancer), genename=str(input_gene))

    if params_miR[0] == '-' and input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        return render_template("allDBnetwork.html", total_data='', total_attr='', tname=tname, tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))

@app.route("/CCLEnetwork")
def CCLEnetwork():
    tname="CCLE"
    tissuename="tissue"
    params_cancer = request.args.get('tissue', '')
    input_gene = request.args.get('gene', '')
    input_term=tname+tissuename+params_cancer+input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_CCLE = '''SELECT id, tissue,gene,tag,gene_TF,TF_target,tissue_name FROM CCLE'''
    curs.execute(sql_count_CCLE)
    result = curs.fetchall()
    genes = list(result)
    input_gene_TF=[]
    params_TF_gene=[]
    for i in genes:
        if params_cancer==i[6] and input_gene==i[2]:
            input_gene_TF.extend(i[4].split(';'))
            params_TF_gene.extend(i[5].split(';'))

    if input_gene_TF[0] != '-' and params_TF_gene[0] == '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1='\\<node id = "-1"><data key = "label">'+input_gene+'</data></node>'
        seg_node.append(node1)
        n=0
        for j in input_gene_TF:
            j=j.strip()
            node2='\\<node id="'+str(n)+'"><data key="label">'+j+'</data></node>'
            edge2 = '\\<edge source="'+str(n)+'" target="-1"></edge>'
            attr2='{ attrValue: '+str(n)+', value: "#50b7c1" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n+=1
        seg_edge.append('\\           </graph>'+'\\'+'\n'+'</graphml>\\')
        totaldata=''.join(seg_node)+''.join(seg_edge)
        totalattr=''.join(seg_attr)
        print totaldata
        print totalattr
        return render_template("allDBnetwork.html",total_data=totaldata,total_attr=totalattr,tname=tname,tissuename=tissuename,cancername=str(params_cancer),genename=str(input_gene))
    if input_gene_TF[0] == '-' and params_TF_gene[0] != '-':
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + input_gene + '</data></node>'
        seg_node.append(node1)
        m = 1000
        for i in params_TF_gene:
            i = i.strip()
            node3 = '\\<node id="' + str(m) + '"><data key="label">' + i + '</data></node>'
            edge3 = '\\<edge source="-1" ' + 'target="' + str(m)+'"></edge>'
            # edge3 = '\\<edge source="' + str(m) + '" target="-1"></edge>'
            attr3 = '{ attrValue: ' + str(m) + ', value: "#B23AEE" },'
            seg_node.append(node3)
            seg_edge.append(edge3)
            seg_attr.append(attr3)
            m += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        print totaldata
        print totalattr
        return render_template("allDBnetwork.html", total_data=totaldata, total_attr=totalattr,tname=tname,tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))
    if input_gene_TF[0] == '-' and params_TF_gene[0] == '-':
        return render_template("allDBnetwork.html", total_data='', total_attr='',tname=tname,tissuename=tissuename,cancername=str(params_cancer), genename=str(input_gene))

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")
    # return render_template("imageflow.html")
@app.route("/download")
def download():
    return render_template("download.html")
@app.route("/help")
def help():
    return render_template("help.html")
@app.route("/search")
def search():
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR FROM TCGA'''
    sql_count_BodyMap = '''SELECT id,tissue,gene,tag,miR FROM EBI'''
    sql_count_CCLE = '''SELECT id,tissue,gene,tag,miR FROM CCLE'''
    sql_count_GTEx = '''SELECT id,tissue,gene,tag,miR FROM GTEx'''
    curs.execute(sql_count_TCGA)
    result_TCGA = curs.fetchall()
    curs.execute(sql_count_BodyMap)
    result_BodyMap = curs.fetchall()
    curs.execute(sql_count_CCLE)
    result_CCLE = curs.fetchall()
    curs.execute(sql_count_GTEx)
    result_GTEx = curs.fetchall()
    genes_TCGA = list(result_TCGA)
    # print genes_TCGA
    genes_BodyMap = list(result_BodyMap)
    genes_CCLE = list(result_CCLE)
    genes_GTEx = list(result_GTEx)
    miRNAtotal = set()
    allmiRNA = []
    for ii in genes_TCGA:
        i = list(ii)
        id, tissue, cancerFullName, cancer, gene, tag, miR = i[0], i[1], i[2], i[3], i[4], i[5], i[6]
        if miR == '-':
            continue
        miRNA = miR.split("; ")
        for j in miRNA:
            j = j.strip().split(": ")[0]
            miRNAtotal.add(j)
    for ii in genes_BodyMap:
        i = list(ii)
        id, tissue, gene, tag, miR = i[0], i[1], i[2], i[3], i[4]
        if miR == '-':
            continue
        miRNA = miR.split("; ")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miRNAtotal.add(j)

    for ii in genes_CCLE:
        i = list(ii)
        id, tissue, gene, tag, miR = i[0], i[1], i[2], i[3], i[4]
        if miR == '-':
            continue
        miRNA = miR.split("; ")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miRNAtotal.add(j)

    for ii in genes_GTEx:
        i = list(ii)
        id, tissue, gene, tag, miR = i[0], i[1], i[2], i[3], i[4]
        if miR == '-':
            continue
        miRNA = miR.split("; ")
        for j in miRNA:
            j = j.strip().split(":")[0]
            miRNAtotal.add(j)

    for line in sorted(list(miRNAtotal)):
        # print line
        a = '<option value = "' + line + '" >' + line + '</option >'
        allmiRNA.append(a)
    input_miRNA = '\n'.join(allmiRNA)

    sql_count_TCGA_TF = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,gene_TF FROM TCGA'''
    sql_count_BodyMap_TF = '''SELECT id,tissue,gene,tag,gene_TF FROM EBI'''
    sql_count_CCLE_TF = '''SELECT id,tissue,gene,tag,gene_TF FROM CCLE'''
    sql_count_GTEx_TF = '''SELECT id,tissue,gene,tag,gene_TF FROM GTEx'''
    curs.execute(sql_count_TCGA_TF)
    result_TCGA_TF = curs.fetchall()
    curs.execute(sql_count_BodyMap_TF)
    result_BodyMap_TF = curs.fetchall()
    curs.execute(sql_count_CCLE_TF)
    result_CCLE_TF = curs.fetchall()
    curs.execute(sql_count_GTEx_TF)
    result_GTEx_TF = curs.fetchall()
    genes_TCGA_TF = list(result_TCGA_TF)
    genes_BodyMap_TF = list(result_BodyMap_TF)
    genes_CCLE_TF = list(result_CCLE_TF)
    genes_GTEx_TF = list(result_GTEx_TF)
    TFtotal = set()
    allTF=[]
    for i in genes_TCGA_TF:
        id, tissue, cancerFullName, cancer, gene, tag, gene_TF = i[0], i[1], i[2], i[3], i[4], i[5], i[6]
        if gene_TF == '-':
            continue
        transfactor = gene_TF.split(";")
        for j in transfactor:
            j = j.strip()
            TFtotal.add(j)

    for i in genes_BodyMap_TF:
        id, tissue, gene, tag, gene_TF = i[0], i[1], i[2], i[3], i[4]
        if gene_TF == '-':
            continue
        transfactor = gene_TF.split(";")
        for j in transfactor:
            j = j.strip()
            TFtotal.add(j)

    for i in genes_CCLE_TF:
        id, tissue, gene, tag, gene_TF = i[0], i[1], i[2], i[3], i[4]
        if gene_TF == '-':
            continue
        transfactor = gene_TF.split(";")
        for j in transfactor:
            j = j.strip()
            TFtotal.add(j)

    for i in genes_GTEx_TF:
        id, tissue, gene, tag, gene_TF = i[0], i[1], i[2], i[3], i[4]
        if gene_TF == '-':
            continue
        transfactor = gene_TF.split(";")
        for j in transfactor:
            j = j.strip()
            TFtotal.add(j)
    for li in sorted(list(TFtotal)):
        # print line
        b = '<option value = "' + li + '" >' + li + '</option >'
        allTF.append(b)
    input_TF = '\n'.join(allTF)
    return render_template("search.html", input_miRNA=input_miRNA,input_TF=input_TF)
@app.route("/searchDataTCGA", methods=['GET','POST'])
def searchDataTCGA():
    input_tumor = request.form.get("cancer","")
    input_TCGA_tumor = input_tumor.encode('gb2312').split("(")[0].strip()
    input_gene = request.form.get("gene","").strip()
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    flag=0
    for i in list(input_gene):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Invalid character input !");document.getElementById("search_gene").value=""; </script>'''
            return render_template("search.html", code=code)
            flag=1
            break
    if flag==0:
        curs = mysql.connection.cursor()
        sql_count_TCGA = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA where cancer="%s" ''' % (input_TCGA_tumor)
        curs.execute(sql_count_TCGA)
        result_TCGA = curs.fetchall()
        genes_TCGA = list(result_TCGA)
        # if input_dataSource_TCGA == "TCGA":
        input_gene = input_gene.strip()
        data_TCGA = []
        data_TCGA2 = []
        for i in genes_TCGA:
            miR_list = []
            miRNA = i[6].split("; ")
            for j in miRNA:
                j = j.strip().split(":")[0]
                miR_list.append(j)
            miR = "; ".join(sorted(miR_list))
            if input_gene==i[4]:
                miR_tuple = (i[0], i[1], i[2], i[3], i[4], i[5],miR,i[7],i[8],i[9])
                data_TCGA.append(miR_tuple)
            if input_gene=='':
                miR_tuple = (i[0], i[1], i[2], i[3], i[4], i[5],miR,i[7],i[8],i[9])
                data_TCGA.append(miR_tuple)
        if data_TCGA:
            
            page = int(request.args.get('page',1 ))
            per_page = int(request.args.get('per_page', len(data_TCGA)))
            pagination = Pagination(page=page, per_page=per_page, total=len(data_TCGA), css_framework='bootstrap3')
            s = (page - 1) * per_page
            e = s + per_page
            numbers = data_TCGA[s:e]
            sum = len(data_TCGA)
            return render_template("TCGA.html", numbers=numbers, sum=sum, pagination=pagination)
        else:
            return render_template("no_data_found.html")
        
@app.route("/searchData", methods=['GET','POST'])
def searchData():
    input_dataSource=request.form.get("dataSource")
    input_cellLine=request.form.get("cellLine")
    input_geneFrom3db = request.form.get("geneFrom3db").strip()
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    flag=0
    for i in list(input_geneFrom3db):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Invalid character input !");document.getElementById("search_gene2").value=""; </script>'''
            return render_template("search.html", code=code)
            flag=1
            break
    if flag==0:
        curs = mysql.connection.cursor()
        sql_count_BodyMap = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Duodenum,Placenta,Lung,Brain,Ovary,Thyroid,Smooth_muscle,Stomach,Endometrium,Heart,Tonsil,Salivary_gland,Breast,Cerebral_cortex,Lymph_node,Spleen,Testis,Skeletal_muscle,Small_intestine,Colon,Liver,Skin,Fallopian_tube,Rectum,Pancreas,Leukocyte,Kidney,Esophagus,Bladder,Bone_marrow,Appendix,Gall_bladder,Prostate FROM EBI'''
        sql_count_CCLE = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Thyroid,Salivary_gland,Soft_tissue,Haematopoietic_and_lymphoid_tissue,Biliary_tract,Pancreas,Central_nervous_system,Small_intestine,Bone,Large_intestine,Autonomic_ganglia,Pleura,Urinary_tract,Lung,Breast,Skin,Ovary,Prostate,Kidney,Upper_aerodigestive_tract,Stomach,Endometrium,Oesophagus,Liver FROM CCLE'''
        sql_count_GTEx = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Artery,Bladder,Brain,Breast,Transformed_fibroblasts,Cervix,Colon,Esophagus,Fallopian_tube,Heart,Kidney,Liver,Lung,Salivary_gland,Muscle,Tibial_nerve,Ovary,Pancreas,Pituitary,Prostate,Skin,Small_intestine,Spleen,Stomach,Testis,Thyroid,Uterus,Vagina,Blood FROM GTEx'''
        curs.execute(sql_count_BodyMap)
        result_BodyMap = curs.fetchall()
        curs.execute(sql_count_CCLE)
        result_CCLE = curs.fetchall()
        curs.execute(sql_count_GTEx)
        result_GTEx = curs.fetchall()
        genes_BodyMap = list(result_BodyMap)
        genes_CCLE = list(result_CCLE)
        genes_GTEx = list(result_GTEx)
        
        if input_dataSource == "BodyMap":
            input_geneFrom3db = input_geneFrom3db.strip()
            data_BodyMap=[]

            for i in genes_BodyMap:
                miR_list = []
                miRNA = i[4].split("; ")
                for j in miRNA:
                    j = j.strip().split(":")[0]
                    miR_list.append(j)
                miR = "; ".join(sorted(miR_list))
                if input_cellLine==i[1] and input_geneFrom3db==i[2]:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i[6],i[7])
                    data_BodyMap.append(miR_tuple)
                if input_cellLine==i[1] and not input_geneFrom3db:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i[6],i[7])
                    data_BodyMap.append(miR_tuple)
                if not input_cellLine and input_geneFrom3db==i[2]:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i[6],i[7])
                    data_BodyMap.append(miR_tuple)
                if not input_cellLine and not input_geneFrom3db:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5], i[6], i[7])
                    data_BodyMap.append(miR_tuple)
            if data_BodyMap:
                page = int(request.args.get('page', 1))
                per_page = int(request.args.get('per_page', len(data_BodyMap)))
                pagination = Pagination(page=page, per_page=per_page, total=len(data_BodyMap), css_framework='bootstrap3')
                s = (page - 1) * per_page
                e = s + per_page
                numbers = data_BodyMap[s:e]
                sum = len(data_BodyMap)
                return render_template("BodyMap.html", numbers=numbers, sum=sum, pagination=pagination)
            if not data_BodyMap:
                return render_template("no_data_found.html")

        if input_dataSource=="CCLE":
            input_geneFrom3db = input_geneFrom3db.strip()
            data_CCLE = []
            for i in genes_CCLE:
                miR_list = []
                i6 = "; ".join(sorted(i[6].split("; ")))
                i7 = "; ".join(sorted(i[7].split("; ")))
                miRNA = i[4].split("; ")
                for j in miRNA:
                    j = j.strip().split(":")[0]
                    miR_list.append(j)
                miR = "; ".join(sorted(miR_list))
                if input_cellLine==i[1] and input_geneFrom3db==i[2]:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6,i7)
                    data_CCLE.append(miR_tuple)
                if input_cellLine==i[1] and not input_geneFrom3db:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6,i7)
                    data_CCLE.append(miR_tuple)
                if not input_cellLine and input_geneFrom3db==i[2]:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6,i7)
                    data_CCLE.append(miR_tuple)
                if not input_cellLine and not input_geneFrom3db:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6,i7)
                    data_CCLE.append(miR_tuple)

            if data_CCLE:
                page = int(request.args.get('page', 1))
                per_page = int(request.args.get('per_page', len(data_CCLE)))
                pagination = Pagination(page=page, per_page=per_page, total=len(data_CCLE), css_framework='bootstrap3')
                s = (page - 1) * per_page
                e = s + per_page
                numbers = data_CCLE[s:e]
                sum = len(data_CCLE)
                return render_template("CCLE.html", numbers=numbers, sum=sum, pagination=pagination)
            if not data_CCLE:
                return render_template("no_data_found.html")

        if input_dataSource == "GTEx":
            input_geneFrom3db = input_geneFrom3db.strip()
            data_GTEx = []
            for i in genes_GTEx:
                miR_list = []
                i6 = "; ".join(sorted(i[6].split("; ")))
                i7 = "; ".join(sorted(i[7].split("; ")))
                miRNA = i[4].split("; ")
                for j in miRNA:
                    j = j.strip().split(":")[0]
                    miR_list.append(j)
                miR = "; ".join(sorted(miR_list))
                if input_cellLine==i[1] and input_geneFrom3db==i[2]:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6,i7)
                    data_GTEx.append(miR_tuple)
                if input_cellLine==i[1] and not input_geneFrom3db:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6,i7)
                    data_GTEx.append(miR_tuple)
                if not input_cellLine and input_geneFrom3db==i[2]:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6,i7)
                    data_GTEx.append(miR_tuple)
                if not input_cellLine and not input_geneFrom3db:
                    miR_tuple = (i[0], i[1], i[2], i[3], miR, i[5],i6,i7)
                    data_GTEx.append(miR_tuple)
            if data_GTEx:
                page = int(request.args.get('page', 1))
                per_page = int(request.args.get('per_page', len(data_GTEx)))
                pagination = Pagination(page=page, per_page=per_page, total=len(data_GTEx), css_framework='bootstrap3')
                s = (page - 1) * per_page
                e = s + per_page
                numbers = data_GTEx[s:e]
                sum = len(data_GTEx)
                return render_template("GTEx.html", numbers=numbers, sum=sum, pagination=pagination)
            if not data_GTEx:
                return render_template("no_data_found.html")

@app.route("/searchAll", methods=['GET','POST'])
def searchAll():
    input_term = request.form.get("term")
    input_term = input_term.encode('gb2312').strip().lower()
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    # print input_term
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id, cancer, gene, tag, miR,gene_TF, TF_target FROM TCGA'''
    sql_count_BodyMap = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM EBI'''
    sql_count_CCLE = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM CCLE'''
    sql_count_GTEx = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM GTEx'''
    curs.execute(sql_count_TCGA)
    result_TCGA = curs.fetchall()
    curs.execute(sql_count_BodyMap)
    result_BodyMap = curs.fetchall()
    curs.execute(sql_count_CCLE)
    result_CCLE = curs.fetchall()
    curs.execute(sql_count_GTEx)
    result_GTEx = curs.fetchall()
    genes_TCGA = list(result_TCGA)
    genes_BodyMap = list(result_BodyMap)
    genes_CCLE = list(result_CCLE)
    genes_GTEx = list(result_GTEx)
    total_data=[]
    for line in genes_TCGA:
        rlt=('TCGA',) + line
        total_data.append(rlt)
    for line in genes_BodyMap:
        rlt=('BodyMap',) + line
        total_data.append(rlt)
    for line in genes_CCLE:
        rlt=('CCLE',) + line
        total_data.append(rlt)
    for line in genes_GTEx:
        rlt=('GTEx',) + line
        total_data.append(rlt)
    total_tissue=set()
    data=[]
    for i in total_data:
        total_tissue.add(i[2].lower())
        tissue=i[2].lower()
        miR_list1 = []
        miR_list2 = []
        miRNA = i[5].split("; ")
        gene=i[3].lower()
        i6="; ".join(sorted(i[6].split('; ')))
        i7 = "; ".join(sorted(i[7].split('; ')))
        for j in miRNA:
            j1 = j.strip().split(": ")[0]
            j2 = j.strip().split(": ")[0].lower()
            miR_list1.append(j1)
            miR_list2.append(j2)
        miR = "; ".join(sorted(miR_list1))
        if input_term == tissue or input_term==gene or input_term in miR_list2 or input_term in ';'.join(miR_list2):
            miR_tuple = (i[0],i[1], i[2], i[3],i[4],miR,i6,i7)
            data.append(miR_tuple)
    if data:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', len(data)))
        pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data[s:e]
        sum = len(data)
        return render_template("searchAll.html", numbers=numbers, sum=sum, pagination=pagination,input_term=input_term)
    if len(data)==0:
        return render_template("no_data_found.html")

@app.route("/methylation")
def methylation():
    params_cancer = request.args.get('cancer', '')
    input_gene = request.args.get('gene', '')
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id, cancer,gene,tag,miR,gene_TF,TF_target,cancer_full_name,tissue,chromsome,methylation,loci_start,loci_end FROM TCGA'''
    curs.execute(sql_count_TCGA)
    result = curs.fetchall()
    genes = list(result)
    for i in genes:
        if params_cancer == i[1] and input_gene == i[2]:
            dic={}
            gene,chr, met,start,end =i[2], i[9], i[10], str(i[11]), str(i[12])
            print start,end
            cap = '<chart caption="Methylation sites of '+gene+ ' TSS" subcaption="Located on transcription start site (TSS) region, forward 2000 bp and backward 200 bp" yaxisname="Beta value" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="92" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Gene name: '+gene+'; '+'Location: Chr'+ chr+': '+start+' - '+end +'"  palette="1" numdivlines="3" theme="ocean">'
            if met != '-':
                met_split=met.split(";")
                for j in met_split:
                    j=j.split(":")
                    dic[j[0].strip()]=j[1]
                a=sorted(dic.keys())
                seg=[]
                for k in a:
                    rlt = '<set label = "'+k+'" value = "'+dic[k]+'" />'
                    seg.append(rlt)
                renderdata=cap+''.join(seg)+"</chart>"
                print renderdata
                return render_template("methylation.html", render_data=renderdata)
            if met=="-":
                renderdata ="There is no methylation sites"
                return render_template("methylation.html", render_data=renderdata)
@app.route("/miRNARegulation")
def miRNARegulation():
    return render_template("miRNARegulation.html")
@app.route("/miRNARegulationO")
def miRNARegulationO():
    params = request.args.get('object', '')
    params = params.encode('gb2312')
    input_term=params
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR FROM TCGA'''
    sql_count_BodyMap = '''SELECT id,tissue,gene,tag,miR FROM EBI'''
    sql_count_CCLE = '''SELECT id,tissue,gene,tag,miR FROM CCLE'''
    sql_count_GTEx = '''SELECT id,tissue,gene,tag,miR FROM GTEx'''
    curs.execute(sql_count_TCGA)
    result_TCGA = curs.fetchall()
    curs.execute(sql_count_BodyMap)
    result_BodyMap = curs.fetchall()
    curs.execute(sql_count_CCLE)
    result_CCLE = curs.fetchall()
    curs.execute(sql_count_GTEx)
    result_GTEx = curs.fetchall()
    genes_TCGA = list(result_TCGA)
    # print genes_TCGA
    genes_BodyMap = list(result_BodyMap)
    genes_CCLE = list(result_CCLE)
    genes_GTEx = list(result_GTEx)
    if params == "TCGA":
        data_TCGA = []
        miR_dic = {}
        for ii in genes_TCGA:
            i=list(ii)
            id,tissue,cancerFullName,cancer,gene,tag,miR = i[0],i[1],i[2],i[3],i[4],i[5],i[6]
            if miR == '-':
                continue
            miRNA=miR.split(";")
            for j in miRNA:
                j = j.split(":")[0]
                cancer_miR= cancer+'\t'+tissue+'\t'+cancerFullName+'\t'+j.strip()
                miR_dic.setdefault(cancer_miR,[]).append(gene)
        # print miR_dic["Adrenal gland\tAdrenocortical carcinoma\tACC\thsa-miR-16-5p"]
        n=0
        key = sorted(miR_dic.keys())
        for k in key:
            v = sorted(miR_dic[k])
            miR_tuple = tuple((k + '\t' + '; '.join(v)+ '\t'+str(n)).split('\t'))
            # print miR_tuple
            n+=1
            data_TCGA.append(miR_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 200))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_TCGA), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_TCGA[s:e]
        sum = len(data_TCGA)
        name="TCGA"
        return render_template("miRNARegulationTCGA.html", numbers=numbers, name=name,sum=sum, pagination=pagination)
    if params == "BodyMap":
        data_BodyMap = []
        miR_dic = {}
        for i in genes_BodyMap:
            id, tissue, gene, tag, miR = i[0],i[1],i[2],i[3],i[4]
            if miR == '-':
                continue
            miRNA = miR.split(";")
            for j in miRNA:
                j = j.split(":")[0]
                cancer_miR = tissue + '\t' + j.strip()
                miR_dic.setdefault(cancer_miR, []).append(gene)
        n=0
        key = sorted(miR_dic.keys())
        for k in key:
            v = sorted(miR_dic[k])
            # miR_tuple= tuple(k+v)+tuple(str(n))
            miR_tuple = tuple((k + '\t' + '; '.join(v)+ '\t'+str(n)).split('\t'))
            n+=1
            data_BodyMap.append(miR_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 200))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_BodyMap), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_BodyMap[s:e]
        sum = len(data_BodyMap)
        name = "BodyMap"
        return render_template("miRNARegulationO.html", name=name,numbers=numbers, sum=sum, pagination=pagination)
    if params == "CCLE":
        data_CCLE = []
        miR_dic = {}
        for i in genes_CCLE:
            id, tissue, gene, tag, miR = i[0],i[1],i[2],i[3],i[4]
            if miR == '-':
                continue
            miRNA=miR.split(";")
            for j in miRNA:
                j = j.split(":")[0]
                cancer_miR= tissue+'\t'+j.strip()
                miR_dic.setdefault(cancer_miR,[]).append(gene)
        print miR_dic['Kidney\thsa-miR-124-3p']
        n=0
        key = sorted(miR_dic.keys())
        for k in key:
            v = sorted(miR_dic[k])
            miR_tuple= tuple((k + '\t' + '; '.join(v)+ '\t'+str(n)).split('\t'))
            n+=1
            data_CCLE.append(miR_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 200))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_CCLE), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_CCLE[s:e]
        sum = len(data_CCLE)
        name= "CCLE"
        return render_template("miRNARegulationO.html", name=name,numbers=numbers, sum=sum, pagination=pagination)
    if params == "GTEx":
        data_GTEx = []
        miR_dic = {}
        for i in genes_GTEx:
            id, tissue, gene, tag, miR = i[0],i[1],i[2],i[3],i[4]
            if miR == '-':
                continue
            miRNA=miR.split(";")
            for j in miRNA:
                j = j.split(":")[0]
                cancer_miR= tissue+'\t'+j.strip()
                miR_dic.setdefault(cancer_miR, []).append(gene)
        n=0
        key = sorted(miR_dic.keys())
        for k in key:
            v = sorted(miR_dic[k])
            miR_tuple =tuple((k + '\t' + '; '.join(v)+ '\t'+str(n)).split('\t'))
            n+=1
            data_GTEx.append(miR_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 200))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_GTEx), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_GTEx[s:e]
        sum = len(data_GTEx)
        name= "GTEx"
        return render_template("miRNARegulationO.html", name=name,numbers=numbers, sum=sum, pagination=pagination)

@app.route("/miRNAnetwork")
def miRNAnetwork():
    dataSource = request.args.get("source")
    input_tissue = request.args.get('tissue')
    input_miRNA = request.args.get('miRNA')
    input_term= dataSource+input_tissue+input_miRNA
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    if dataSource == "TCGA":
        sql = '''SELECT id,cancer,gene,tag,miR,gene_TF,TF_target FROM TCGA WHERE cancer="%s" and  miR like "%%%s%%"''' % (input_tissue, input_miRNA)
        print sql
    if dataSource == "BodyMap":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM EBI WHERE tissue="%s" and miR like "%%%s%%"''' % (input_tissue, input_miRNA)
    if dataSource == "CCLE":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM CCLE WHERE tissue="%s" and miR like "%%%s%%"''' % (input_tissue, input_miRNA)
    if dataSource == "GTEx":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM GTEx where tissue="%s" and miR like "%%%s%%"''' % (input_tissue, input_miRNA)
    curs.execute(sql)
    result = curs.fetchall()
    genes = list(result)
    print genes
    dic_miRNA={}
    
    downdata=[]
    for i in genes:
        gene=i[2]
        for g in gene.split('; '):
            downdata.append(input_miRNA+','+g)
        dic_miRNA.setdefault(input_miRNA,[]).append(gene)
    download_data='miRNA,gene'+'\\n'+'\\n'.join(downdata)
    for k,v in dic_miRNA.iteritems():
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + k + '</data></node>'
        seg_node.append(node1)
        n = 0
        for j in v:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="-1" ' + 'target="' + str(n) + '"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#EEEE00" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("miRNAnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, miRNA=str(input_miRNA), dataSource=str(dataSource), input_tissue=str(input_tissue))

@app.route("/TFnetwork")
def TFnetwork():
    dataSource = request.args.get("source")
    input_tissue = request.args.get('tissue')
    input_tissue = input_tissue.encode('gb2312')
    input_TF = request.args.get('TF')
    input_term=dataSource+input_tissue+input_TF
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    if dataSource == "TCGA":
        sql = '''SELECT id,cancer,gene,tag,miR,gene_TF,TF_target FROM TCGA WHERE cancer="%s" and  gene_TF like "%%%s%%"''' % (input_tissue, input_TF)
        print sql
    if dataSource == "BodyMap":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM EBI WHERE tissue="%s" and gene_TF like "%%%s%%"''' % (input_tissue, input_TF)
    if dataSource == "CCLE":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM CCLE WHERE tissue="%s" and gene_TF like "%%%s%%"''' % (input_tissue, input_TF)
    if dataSource == "GTEx":
        sql = '''SELECT id,tissue,gene,tag,miR,gene_TF,TF_target FROM GTEx where tissue="%s" and gene_TF like "%%%s%%"''' % (input_tissue, input_TF)
    curs.execute(sql)
    result = curs.fetchall()
    genes = list(result)
    print genes
    dic_tf={}
    
    downdata=[]
    for i in genes:
        gene=i[2]
        for g in gene.split('; '):
            downdata.append(input_TF+','+g)
        dic_tf.setdefault(input_TF,[]).append(gene)
    download_data='TF,gene'+'\\n'+'\\n'.join(downdata)
    for k,v in dic_tf.iteritems():
        seg_node = []
        seg_edge = []
        seg_attr = []
        seg_node.append('\\<graphml>\\<key id="label" for="all" attr.name="label" attr.type="string"/>\\<key id="weight" for="node" attr.name="weight" attr.type="double"/>\\<graph edgedefault="directed">')
        node1 = '\\<node id = "-1"><data key = "label">' + k + '</data></node>'
        seg_node.append(node1)
        n = 0
        for j in v:
            j = j.strip()
            node2 = '\\<node id="' + str(n) + '"><data key="label">' + j + '</data></node>'
            edge2 = '\\<edge source="-1" ' + 'target="' + str(n) + '"></edge>'
            attr2 = '{ attrValue: ' + str(n) + ', value: "#EEEE00" },'
            seg_node.append(node2)
            seg_edge.append(edge2)
            seg_attr.append(attr2)
            n += 1
        seg_edge.append('\\           </graph>' + '\\' + '\n' + '</graphml>\\')
        totaldata = ''.join(seg_node) + ''.join(seg_edge)
        totalattr = ''.join(seg_attr)
        return render_template("TFnetwork.html", download_data=download_data,total_data=totaldata, total_attr=totalattr, tf=str(input_TF), dataSource=str(dataSource), input_tissue=str(input_tissue))
@app.route("/TFRegulation")
def TFRegulation():
    return render_template("TFRegulation.html")

@app.route("/TFRegulationO")
def TFRegulationO():
    params = request.args.get('object', '')
    input_term=params
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,gene_TF FROM TCGA'''
    sql_count_BodyMap = '''SELECT id,tissue,gene,tag,gene_TF FROM EBI'''
    sql_count_CCLE = '''SELECT id,tissue,gene,tag,gene_TF FROM CCLE'''
    sql_count_GTEx = '''SELECT id,tissue,gene,tag,gene_TF FROM GTEx'''
    curs.execute(sql_count_TCGA)
    result_TCGA = curs.fetchall()
    curs.execute(sql_count_BodyMap)
    result_BodyMap = curs.fetchall()
    curs.execute(sql_count_CCLE)
    result_CCLE = curs.fetchall()
    curs.execute(sql_count_GTEx)
    result_GTEx = curs.fetchall()
    genes_TCGA = list(result_TCGA)
    # print genes_TCGA
    genes_BodyMap = list(result_BodyMap)
    genes_CCLE = list(result_CCLE)
    genes_GTEx = list(result_GTEx)
    if params == "TCGA":
        data_TCGA = []
        TF_dic = {}
        for i in genes_TCGA:
            id,tissue,cancerFullName,cancer,gene,tag,gene_TF = i[0],i[1],i[2],i[3],i[4],i[5],i[6]
            if gene_TF == '-':
                continue
            transfactor=gene_TF.split(";")
            for j in transfactor:
                j = j.strip()
                cancer_TF_gene= cancer+'\t'+tissue+'\t'+cancerFullName+'\t'+j
                TF_dic.setdefault(cancer_TF_gene,[]).append(gene)
        n=0
        key = sorted(TF_dic.keys())
        for k in key:
            v = sorted(TF_dic[k])
            TF_tuple = tuple((k + '\t' + '; '.join(v)+ '\t'+str(n)).split('\t'))
            n+=1
            data_TCGA.append(TF_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 200))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_TCGA), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_TCGA[s:e]
        sum = len(data_TCGA)
        name="TCGA"
        return render_template("TFRegulationTCGA.html", name=name,numbers=numbers, sum=sum, pagination=pagination)
    if params == "BodyMap":
        data_BodyMap = []
        TF_dic = {}
        for i in genes_BodyMap:
            id, tissue, gene, tag, gene_TF = i[0],i[1],i[2],i[3],i[4]
            if gene_TF == '-':
                continue
            transfactor = gene_TF.split(";")
            for j in transfactor:
                j = j.strip()
                tissue_TF_gene = tissue + '\t' + j
                TF_dic.setdefault(tissue_TF_gene, []).append(gene)
        n=0
        key = sorted(TF_dic.keys())
        for k in key:
            v = sorted(TF_dic[k])
            TF_tuple = tuple((k + '\t' + '; '.join(v)+ '\t'+str(n)).split('\t'))
            n+=1
            data_BodyMap.append(TF_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 200))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_BodyMap), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_BodyMap[s:e]
        sum = len(data_BodyMap)
        name = "BodyMap"
        return render_template("TFRegulationO.html", name=name,numbers=numbers, sum=sum, pagination=pagination)
    if params == "CCLE":
        data_CCLE = []
        TF_dic = {}
        for i in genes_CCLE:
            id, tissue, gene, tag, gene_TF = i[0],i[1],i[2],i[3],i[4]
            if gene_TF == '-':
                continue
            transfactor=gene_TF.split(";")
            for j in transfactor:
                j = j.strip()
                tissue_TF_gene= tissue+'\t'+j
                TF_dic.setdefault(tissue_TF_gene,[]).append(gene)
        n=0
        key = sorted(TF_dic.keys())
        for k in key:
            v=sorted(TF_dic[k])
            TF_tuple= tuple((k + '\t' + '; '.join(v)+ '\t'+str(n)).split('\t'))
            n+=1
            data_CCLE.append(TF_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 200))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_CCLE), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_CCLE[s:e]
        sum = len(data_CCLE)
        name= "CCLE"
        return render_template("TFRegulationO.html", name=name,numbers=numbers, sum=sum, pagination=pagination)
    if params == "GTEx":
        data_GTEx = []
        TF_dic = {}
        for i in genes_GTEx:
            id, tissue, gene, tag, gene_TF = i[0],i[1],i[2],i[3],i[4]
            if gene_TF == '-':
                continue
            transfactor=gene_TF.split(";")
            for j in transfactor:
                j = j.strip()
                tissue_TF_gene= tissue+'\t'+j
                TF_dic.setdefault(tissue_TF_gene, []).append(gene)
        n=0
        key = sorted(TF_dic.keys())
        for k in key:
            v = sorted(TF_dic[k])
            TF_tuple =tuple((k + '\t' + '; '.join(v)+ '\t'+str(n)).split('\t'))
            n+=1
            data_GTEx.append(TF_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 200))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_GTEx), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_GTEx[s:e]
        sum = len(data_GTEx)
        name= "GTEx"
        return render_template("TFRegulationO.html", name=name,numbers=numbers, sum=sum, pagination=pagination)

@app.route("/browsegene")
def browsegene():
    params = request.args.get('object', '')
    input_term=params
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    if params == "TCGA":
        sql_count_TCGA = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA'''
        curs.execute(sql_count_TCGA)
        result_TCGA = curs.fetchall()
        genes_TCGA = list(result_TCGA)
        data_TCGA = []
        dic = {}
        dic_cancer_fullname={}
        for i in genes_TCGA:
            id, tissue, cancerFullName, cancer, gene, tag = i[0], i[1], i[2], i[3], i[4], i[5]
            gene_tag = gene + '\t' + tag
            dic.setdefault(gene_tag, []).append(cancer)
        n = 1
        key = sorted(dic.keys())
        for k in key:
            v = sorted(dic[k])
            R_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            # print R_tuple
            n += 1
            data_TCGA.append(R_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_TCGA), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_TCGA[s:e]
        sum = len(data_TCGA)
        return render_template("TCGAgene.html", numbers=numbers, sum=sum, pagination=pagination)
    if params == "BodyMap":
        sql_count_BodyMap = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Duodenum,Placenta,Lung,Brain,Ovary,Thyroid,Smooth_muscle,Stomach,Endometrium,Heart,Tonsil,Salivary_gland,Breast,Cerebral_cortex,Lymph_node,Spleen,Testis,Skeletal_muscle,Small_intestine,Colon,Liver,Skin,Fallopian_tube,Rectum,Pancreas,Leukocyte,Kidney,Esophagus,Bladder,Bone_marrow,Appendix,Gall_bladder,Prostate FROM EBI'''
        curs.execute(sql_count_BodyMap)
        result_BodyMap = curs.fetchall()
        genes_BodyMap = list(result_BodyMap)
        data_BodyMap = []
        dic = {}
        for i in genes_BodyMap:
            id, tissue, gene, tag = i[0], i[1], i[2], i[3]
            gene_tag = gene + '\t' + tag
            dic.setdefault(gene_tag, []).append(tissue)
        n = 1
        key = sorted(dic.keys())
        print dic
        for k in key:
            v = sorted(dic[k])
            R_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            # print R_tuple
            n += 1
            data_BodyMap.append(R_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_BodyMap), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_BodyMap[s:e]
        sum = len(data_BodyMap)
        return render_template("BodyMapgene.html", numbers=numbers, sum=sum, pagination=pagination)
    if params == "CCLE":
        sql_count_CCLE = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Thyroid,Salivary_gland,Soft_tissue,Haematopoietic_and_lymphoid_tissue,Biliary_tract,Pancreas,Central_nervous_system,Small_intestine,Bone,Large_intestine,Autonomic_ganglia,Pleura,Urinary_tract,Lung,Breast,Skin,Ovary,Prostate,Kidney,Upper_aerodigestive_tract,Stomach,Endometrium,Oesophagus,Liver FROM CCLE'''
        curs.execute(sql_count_CCLE)
        result_CCLE = curs.fetchall()
        genes_CCLE = list(result_CCLE)
        data_CCLE = []
        dic = {}
        for i in genes_CCLE:
            id, tissue, gene, tag = i[0], i[1], i[2], i[3]
            gene_tag = gene + '\t' + tag
            dic.setdefault(gene_tag, []).append(tissue)
        n = 1
        key = sorted(dic.keys())
        for k in key:
            v = sorted(dic[k])
            R_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            # print R_tuple
            n += 1
            data_CCLE.append(R_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_CCLE), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_CCLE[s:e]
        sum = len(data_CCLE)
        return render_template("CCLEgene.html", numbers=numbers, sum=sum, pagination=pagination)
    if params == "GTEx":
        sql_count_GTEx = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Artery,Bladder,Brain,Breast,Transformed_fibroblasts,Cervix,Colon,Esophagus,Fallopian_tube,Heart,Kidney,Liver,Lung,Salivary_gland,Muscle,Tibial_nerve,Ovary,Pancreas,Pituitary,Prostate,Skin,Small_intestine,Spleen,Stomach,Testis,Thyroid,Uterus,Vagina,Blood FROM GTEx'''
        curs.execute(sql_count_GTEx)
        result_GTEx = curs.fetchall()
        genes_GTEx = list(result_GTEx)
        data_GTEx = []
        dic = {}
        for i in genes_GTEx:
            id, tissue, gene, tag = i[0], i[1], i[2], i[3]
            gene_tag = gene + '\t' + tag
            dic.setdefault(gene_tag, []).append(tissue)
        n = 1
        key = sorted(dic.keys())
        for k in key:
            v = sorted(dic[k])
            R_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            # print R_tuple
            n += 1
            data_GTEx.append(R_tuple)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 100))
        pagination = Pagination(page=page, per_page=per_page, total=len(data_GTEx), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = data_GTEx[s:e]
        sum = len(data_GTEx)
        return render_template("GTExgene.html", numbers=numbers, sum=sum, pagination=pagination)

@app.route("/expBarplotTCGAgene")
def expBarplotTCGAgene():
    input_gene = request.args.get('gene', '')
    input_term=input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_TCGA_exp = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR,TF_or_gene,gene_TF,TF_target,BLCA,HNSC,THCA,PRAD,ACC,KICH,UVM,THYM,MESO,CHOL,STES,OV,UCEC,LUAD,COAD,BRCA,DLBC,KIRC,STAD,LGG,READ1,ESCA,LAML,LIHC,GBM,KIRP,PCPG,UCS,LUSC,TGCT,SARC,SKCM,CESC,PAAD FROM TCGA where gene="%s"''' % (input_gene)
    curs.execute(sql_TCGA_exp)
    result = curs.fetchall()
    genes = list(result)
    # s=set()
    for i in genes:
        # if input_gene == i[4]:
        gene=i[4]
        cancer_name=["BLCA","HNSC","THCA","PRAD","ACC","KICH","UVM","THYM","MESO","CHOL","STES","OV","UCEC","LUAD","COAD","BRCA","DLBC","KIRC","STAD","LGG","READ","ESCA","LAML","LIHC","GBM","KIRP","PCPG","UCS","LUSC","TGCT","SARC","SKCM","CESC","PAAD"]
        exp=i[10:]
        dic=dict(zip(cancer_name,exp))
        cap = '<chart caption="Expression level of gene '+gene+' in different cancers"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Cancer name"  palette="1" numdivlines="3" theme="ocean">'
        a = sorted(dic.keys())
        seg = []
        for k in a:
            rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
            seg.append(rlt)
        renderdata = cap + ''.join(seg) + "</chart>"
        return render_template("cancerExp.html", render_data=renderdata)

@app.route("/expBarplotBodyMapgene")
def expBarplotBodyMapgene():
    input_gene = request.args.get('gene', '')
    input_term=input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_BodyMap_exp = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Duodenum,Placenta,Lung,Brain,Ovary,Thyroid,Smooth_muscle,Stomach,Endometrium,Heart,Tonsil,Salivary_gland,Breast,Cerebral_cortex,Lymph_node,Spleen,Testis,Skeletal_muscle,Small_intestine,Colon,Liver,Skin,Fallopian_tube,Rectum,Pancreas,Leukocyte,Kidney,Esophagus,Bladder,Bone_marrow,Appendix,Gall_bladder,Prostate FROM EBI where gene="%s"''' % (input_gene)    
    curs.execute(sql_BodyMap_exp)
    result = curs.fetchall()
    genes = list(result)
    for i in genes:
        gene=i[2]
        tissue_name=["Adipose","Adrenal gland","Duodenum","Placenta","Lung","Brain","Ovary","Thyroid","Smooth muscle","Stomach","Endometrium","Heart","Tonsil","Salivary gland","Breast","Cerebral cortex","Lymph node","Spleen","Testis","Skeletal muscle","Small intestine","Colon","Liver","Skin","Fallopian tube","Rectum","Pancreas","Leukocyte","Kidney","Esophagus","Bladder","Bone marrow","Appendix","Gall bladder","Prostate"]
        exp=i[8:]
        print len(tissue_name)
        print len(exp)
        dic=dict(zip(tissue_name,exp))
        print dic
        cap = '<chart caption="Expression level of gene '+gene+' in different tissues"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Cancer name"  palette="1" numdivlines="3" theme="ocean">'
        a = sorted(dic.keys())
        seg = []
        for k in a:
            rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
            seg.append(rlt)
        renderdata = cap + ''.join(seg) + "</chart>"
        return render_template("cancerExp.html", render_data=renderdata)


@app.route("/expBarplotCCLEgene")
def expBarplotCCLEgene():
    input_gene = request.args.get('gene', '')
    input_term=input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_CCLE_exp = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Thyroid,Salivary_gland,Soft_tissue,Haematopoietic_and_lymphoid_tissue,Biliary_tract,Pancreas,Central_nervous_system,Small_intestine,Bone,Large_intestine,Autonomic_ganglia,Pleura,Urinary_tract,Lung,Breast,Skin,Ovary,Prostate,Kidney,Upper_aerodigestive_tract,Stomach,Endometrium,Oesophagus,Liver FROM CCLE where gene="%s"''' % (input_gene)
    curs.execute(sql_CCLE_exp)
    result = curs.fetchall()
    genes = list(result)
    # s=set()
    for i in genes:
        gene = i[2]
        tissue_name = ["Thyroid", "Salivary gland", "Soft tissue", "Haematopoietic and lymphoid tissue","Biliary tract", "Pancreas", "Central nervous system", "Small intestine", "Bone", "Large intestine", "Autonomic ganglia", "Pleura", "Urinary tract", "Lung", "Breast", "Skin","Ovary", "Prostate", "Kidney", "Upper aerodigestive tract", "Stomach", "Endometrium","Oesophagus", "Liver"]
        exp = i[8:]
        dic = dict(zip(tissue_name, exp))
        print dic
        cap = '<chart caption="Expression level of gene ' + gene + ' in different tissues"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Cancer name"  palette="1" numdivlines="3" theme="ocean">'
        a = sorted(dic.keys())
        seg = []
        for k in a:
            rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
            seg.append(rlt)
        renderdata = cap + ''.join(seg) + "</chart>"
        return render_template("cancerExp.html", render_data=renderdata)

@app.route("/expBarplotGTExgene")
def expBarplotGTExgene():
    input_gene = request.args.get('gene', '')
    input_term=input_gene
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_GTEx_exp = '''SELECT id,tissue,gene,tag,miR,TF_or_gene,gene_TF,TF_target,Adipose,Adrenal_gland,Artery,Bladder,Brain,Breast,Transformed_fibroblasts,Cervix,Colon,Esophagus,Fallopian_tube,Heart,Kidney,Liver,Lung,Salivary_gland,Muscle,Tibial_nerve,Ovary,Pancreas,Pituitary,Prostate,Skin,Small_intestine,Spleen,Stomach,Testis,Thyroid,Uterus,Vagina,Blood FROM GTEx where gene="%s"''' % (input_gene)
    curs.execute(sql_GTEx_exp)
    result = curs.fetchall()
    genes = list(result)
    for i in genes:
        gene = i[2]
        tissue_name = ["Adipose", "Adrenal gland", "Artery", "Bladder", "Brain", "Breast","Transformed fibroblasts", "Cervix", "Colon", "Esophagus", "Fallopian tube", "Heart","Kidney", "Liver", "Lung", "Salivary gland", "Muscle", "Tibial nerve", "Ovary", "Pancreas","Pituitary", "Prostate", "Skin", "Small intestine", "Spleen", "Stomach", "Testis", "Thyroid","Uterus", "Vagina", "Blood"]
        exp = i[8:]
        dic = dict(zip(tissue_name, exp))
        cap = '<chart caption="Expression level of gene ' + gene + ' in different tissues"' + ' yaxisname="FPKM" yaxismaxvalue="1" showLabels="1" xAxisNamePadding="0" rotateValues="1" formatNumberScale="0" showCanvasBorder="0" bgColor="#D1D1D1" yAxisNamePadding="10" maxLabelHeight="300" divLineAlpha="30" divLineIsDashed="0" valueFontBold="0" xAxisNameFontSize="18" xAxisNameFontBold="1" showBorder="0" borderThickness="0" outcnvbasefont="Arial" showYAxisValues="0"  canvasPadding="20" plotSpacePercent="50" baseFontSize="14" captionFontSize="24" subCaptionFontSize="20" outcnvbasefontsize="20" outcnvbasefontcolor="#404040" labelDisplay="Rotate" slantLabels="1" labelFontSize="12" xaxisname="Cancer name"  palette="1" numdivlines="3" theme="ocean">'
        a = sorted(dic.keys())
        seg = []
        for k in a:
            rlt = '<set label = "' + k + '" value = "' + str(dic[k]) + '" />'
            seg.append(rlt)
        renderdata = cap + ''.join(seg) + "</chart>"
        return render_template("cancerExp.html", render_data=renderdata)

@app.route("/miRNAsearch",methods=['GET','POST'])
def miRNAsearch():
    input_dataSource_miRNA = request.form.get("datafrom1")
    input_miRNA = request.form.get("miRNA")
    input_term=input_dataSource_miRNA+input_miRNA
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    sql=''
    curs = mysql.connection.cursor()
    if input_dataSource_miRNA == "TCGA":
        sql_tcga = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,miR FROM TCGA where miR like "%%%s%%"''' % (input_miRNA)
        curs.execute(sql_tcga)
        result = curs.fetchall()
        genes = list(result)
        data = []
        renddata=[]
        miR_dic = {}
        for ii in genes:
            i = list(ii)
            id, tissue, cancerFullName, cancer, gene, tag, miR = i[0], i[1], i[2], i[3], i[4], i[5], i[6]
            if miR == '-':
                continue
            miRNA = miR.split("; ")
            for j in miRNA:
                j = j.strip().split(": ")[0]
                cancer_miR = cancer + '\t' + tissue + '\t' + cancerFullName + '\t' + j.strip()
                miR_dic.setdefault(cancer_miR, []).append(gene)
        n = 0
        key = sorted(miR_dic.keys())
        for k in key:
            v = sorted(miR_dic[k])
            miR_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            n += 1
            data.append(miR_tuple)
        for jj in data:
            if input_miRNA==jj[3]:
                renddata.append(jj)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', len(renddata)))
        pagination = Pagination(page=page, per_page=per_page, total=len(renddata), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = renddata[s:e]
        sum = len(renddata)
        return render_template("miRNARegulationTCGA.html", name=input_dataSource_miRNA, miRNAname=input_miRNA,numbers=numbers, sum=sum, pagination=pagination)
    
    if input_dataSource_miRNA == "BodyMap":
        sql = '''SELECT id,tissue,gene,tag,miR FROM EBI where miR like "%%%s%%"''' % (input_miRNA)
    if input_dataSource_miRNA == "CCLE":
        sql = '''SELECT id,tissue,gene,tag,miR FROM CCLE where miR like "%%%s%%"''' % (input_miRNA)
    if input_dataSource_miRNA == "GTEx":
        sql = '''SELECT id,tissue,gene,tag,miR FROM GTEx where miR like "%%%s%%"''' % (input_miRNA)
    
    if input_dataSource_miRNA != "TCGA":
        curs.execute(sql)
        result = curs.fetchall()
        genes = list(result)
        data = []
        miR_dic = {}
        renddata=[]
        for ii in genes:
            i = list(ii)
            id, tissue, gene, tag, miR = i[0], i[1], i[2], i[3], i[4]
            if miR == '-':
                continue
            miRNA = miR.split("; ")
            for j in miRNA:
                j = j.strip().split(":")[0]
                # miRNAtotal.add(j)
                cancer_miR = tissue + '\t' + j.strip()
                miR_dic.setdefault(cancer_miR, []).append(gene)
        n = 0
        key = sorted(miR_dic.keys())
        for k in key:
            v = sorted(miR_dic[k])
            miR_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            n += 1
            data.append(miR_tuple)
        for jj in data:
            if input_miRNA==jj[1]:
                renddata.append(jj)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', len(renddata)))
        pagination = Pagination(page=page, per_page=per_page, total=len(renddata), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = renddata[s:e]
        sum = len(renddata)
        return render_template("miRNARegulationO.html", name=input_dataSource_miRNA, miRNAname=input_miRNA,numbers=numbers, sum=sum, pagination=pagination)
        
@app.route("/TFsearch",methods=['GET','POST'])
def TFsearch():
    input_dataSource_TF = request.form.get("datafrom2")
    input_TF = request.form.get("TF")
    input_term=input_dataSource_TF+input_TF
    alphas_digit = string.ascii_letters + '_+-.\\\t '  + string.digits
    for i in list(input_term):
        if i not in alphas_digit:
            code='''<script type="text/javascript"> alert("Sorry, your input contains illegal characters !");document.getElementById("clear").value=""; </script>'''
            return render_template("homepage.html",code=code)
            break
    curs = mysql.connection.cursor()
    sql_count_TCGA = '''SELECT id,tissue,cancerFullName,cancer,gene,tag,gene_TF FROM TCGA'''
    sql_count_BodyMap = '''SELECT id,tissue,gene,tag,gene_TF FROM EBI'''
    sql_count_CCLE = '''SELECT id,tissue,gene,tag,gene_TF FROM CCLE'''
    sql_count_GTEx = '''SELECT id,tissue,gene,tag,gene_TF FROM GTEx'''
    curs.execute(sql_count_TCGA)
    result_TCGA = curs.fetchall()
    curs.execute(sql_count_BodyMap)
    result_BodyMap = curs.fetchall()
    curs.execute(sql_count_CCLE)
    result_CCLE = curs.fetchall()
    curs.execute(sql_count_GTEx)
    result_GTEx = curs.fetchall()
    genes_TCGA = list(result_TCGA)
    genes_BodyMap = list(result_BodyMap)
    genes_CCLE = list(result_CCLE)
    genes_GTEx = list(result_GTEx)
    if input_dataSource_TF == "TCGA":
        data_TCGA = []
        TF_dic = {}
        renddata=[]
        for i in genes_TCGA:
            id, tissue, cancerFullName, cancer, gene, tag, gene_TF = i[0], i[1], i[2], i[3], i[4], i[5], i[6]
            if gene_TF == '-':
                continue
            transfactor = gene_TF.split(";")
            for j in transfactor:
                j = j.strip()
                cancer_TF_gene = cancer + '\t' + tissue + '\t' + cancerFullName + '\t' + j
                TF_dic.setdefault(cancer_TF_gene, []).append(gene)
        n = 0
        key = sorted(TF_dic.keys())
        for k in key:
            v = sorted(TF_dic[k])
            TF_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            n += 1
            data_TCGA.append(TF_tuple)

        for jj in data_TCGA:
            if input_TF==jj[3]:
                renddata.append(jj)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', len(renddata)))
        pagination = Pagination(page=page, per_page=per_page, total=len(renddata), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = renddata[s:e]
        sum = len(renddata)
        name = "TCGA"
        TFname=numbers[0][3]
        return render_template("TFRegulationTCGA.html", name=name, TFname=TFname,numbers=numbers, sum=sum, pagination=pagination)
    if input_dataSource_TF == "BodyMap":
        data_BodyMap = []
        TF_dic = {}
        renddata=[]
        for i in genes_BodyMap:
            id, tissue, gene, tag, gene_TF = i[0], i[1], i[2], i[3], i[4]
            if gene_TF == '-':
                continue
            transfactor = gene_TF.split(";")
            for j in transfactor:
                j = j.strip()
                tissue_TF_gene = tissue + '\t' + j
                TF_dic.setdefault(tissue_TF_gene, []).append(gene)
        n = 0
        key = sorted(TF_dic.keys())
        for k in key:
            v = sorted(TF_dic[k])
            TF_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            n += 1
            data_BodyMap.append(TF_tuple)
        for jj in data_BodyMap:
            if input_TF==jj[1]:
                renddata.append(jj)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', len(renddata)))
        pagination = Pagination(page=page, per_page=per_page, total=len(renddata), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = renddata[s:e]
        sum = len(renddata)
        name = "BodyMap"
        TFname = numbers[0][1]
        return render_template("TFRegulationO.html", name=name, TFname=TFname,numbers=numbers, sum=sum, pagination=pagination)

    if input_dataSource_TF == "CCLE":
        data_CCLE = []
        TF_dic = {}
        renddata=[]
        for i in genes_CCLE:
            id, tissue, gene, tag, gene_TF = i[0], i[1], i[2], i[3], i[4]
            if gene_TF == '-':
                continue
            transfactor = gene_TF.split(";")
            for j in transfactor:
                j = j.strip()
                tissue_TF_gene = tissue + '\t' + j
                TF_dic.setdefault(tissue_TF_gene, []).append(gene)
        n = 0
        key = sorted(TF_dic.keys())
        for k in key:
            v = sorted(TF_dic[k])
            TF_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            n += 1
            data_CCLE.append(TF_tuple)
        for jj in data_CCLE:
            if input_TF==jj[1]:
                renddata.append(jj)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', len(renddata)))
        pagination = Pagination(page=page, per_page=per_page, total=len(renddata), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = renddata[s:e]
        sum = len(renddata)
        name = "CCLE"
        TFname = numbers[0][1]
        return render_template("TFRegulationO.html", name=name, TFname=TFname,numbers=numbers, sum=sum, pagination=pagination)

    if input_dataSource_TF == "GTEx":
        data_GTEx = []
        TF_dic = {}
        renddata=[]
        for i in genes_GTEx:
            id, tissue, gene, tag, gene_TF = i[0], i[1], i[2], i[3], i[4]
            if gene_TF == '-':
                continue
            transfactor = gene_TF.split(";")
            for j in transfactor:
                j = j.strip()
                tissue_TF_gene = tissue + '\t' + j
                TF_dic.setdefault(tissue_TF_gene, []).append(gene)
        n = 0
        key = sorted(TF_dic.keys())
        for k in key:
            v = sorted(TF_dic[k])
            TF_tuple = tuple((k + '\t' + '; '.join(v) + '\t' + str(n)).split('\t'))
            n += 1
            data_GTEx.append(TF_tuple)
        for jj in data_GTEx:
            if input_TF==jj[1]:
                renddata.append(jj)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', len(renddata)))
        pagination = Pagination(page=page, per_page=per_page, total=len(renddata), css_framework='bootstrap3')
        s = (page - 1) * per_page
        e = s + per_page
        numbers = renddata[s:e]
        sum = len(renddata)
        name = "GTEx"
        TFname = numbers[0][1]
        return render_template("TFRegulationO.html", name=name, TFname=TFname,numbers=numbers, sum=sum, pagination=pagination)
