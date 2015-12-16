from org.apache.pig.scripting import Pig 

limit_count = 3
hash_count = 20

load_master = """%s = LOAD './%s.csv' USING PigStorage(',') as (FeatureID:int, ImageID:int,""" %("master", "database")
load_query = """%s = LOAD './%s.csv' USING PigStorage(',') as (FeatureID:int, ImageID:int,""" %("queryall", "query")
indi_hash = ""
group = ""
store_out = ""
for i in range(1,hash_count+1):
	load_master = load_master + "T" + str(i) + ":int"
	load_query = load_query + "T" + str(i) + ":int"
	if i == hash_count:
		load_master += ");\n"
		load_query += ");\n"
	else:
		load_master += ","
		load_query += ","
	indi_hash += "t" + str(i) + " = "
	indi_hash += """FOREACH master GENERATE FeatureID,ImageID,T""" + str(i) + ";\n"
	group +="gt" + str(i) + " = " + "GROUP t" + str(i) + " BY T" + str(i) + ";\n"
	store_out += "STORE gt" + str(i) + " INTO 'gt" + str(i) + ".out';\n"

pig_script = load_master + indi_hash + group + store_out
Pig.compile(pig_script).bind().runSingle()


pig_script = ""
pig_script += "set io.sort.mb 10;\n"
load_out = ""
indi_hash_q = ""
count_all = ""
last_command = "m = UNION"
for i in range(1,hash_count+1):
	load_out += """f%d = LOAD './gt%d.out/part-r-00000' using PigStorage('\\t') as (group:int, featurebag:{feature:(FeatureID:int, ImageID:int, Hash:int)});\n""" % (i, i)
	indi_hash_q += "q" + str(i) + " = "
	indi_hash_q += """FOREACH queryall GENERATE FeatureID,ImageID,T""" + str(i) + ";\n"
	temp_count = ""
	temp_count += "t%d =  foreach master generate FeatureID, ImageID, T%d;\n" %(i,i)
	temp_count += "g%d = join q%d by T%d, f%d by group;\n" % (i,i,i,i)
	temp_count += "g%d = foreach g%d generate flatten(featurebag);\n" %(i,i)
	temp_count += "m%d = group g%d by ImageID;\n" %(i,i)
	temp_count += "m%d = foreach m%d generate group, COUNT(g%d);\n" %(i,i,i)
	temp_count += "m%d = order m%d by $%d DESC;\n" %(i,i,1)
	temp_count += "m%d = LIMIT m%d %d;\n" %(i,i,limit_count)
	count_all += temp_count
	if i == hash_count:
		last_command += " m%d;\n" % i
	else:
		last_command += " m%d," % i





pig_script += load_out + load_master + load_query + indi_hash_q + count_all + last_command + "STORE m into 'pig.result';\n"
Pig.compile(pig_script).bind().runSingle()

