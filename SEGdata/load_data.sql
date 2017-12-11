load data local infile "/home/tangq/SEG/SEGdata/TCGAmysqldata.xls" into table TCGA FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
load data local infile "/home/tangq/SEG/SEGdata/CCLEmysqldata.xls" into table CCLE FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
load data local infile "/home/tangq/SEG/SEGdata/EBImysqldata.xls" into table EBI FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
load data local infile "/home/tangq/SEG/SEGdata/GTExmysqldata.xls" into table GTEx FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n';
