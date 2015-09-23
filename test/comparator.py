#!/usr/bin/python

import re
import glob
import os

class Statist(object):
	total_comps=0 # total number of analysis 
	same_files=0 # cases with exactly the same files in both reports
	new_files=0 # cases with new files in the hardened one
	timedout=0 # report hitted time-out
	no_dropped=0 # report without drops
	# Total = same + new + same_name + timedout + no_dropped
	similar_files=0 # cases with files with same name but different size (<100 bytes)
	less_similar_files=0 # cases with files with same name but different size (>100 bytes)
	# same_name = similar + less_similar
	
	diff_types=0 # cases with files that differs in the type field
	
	anomalies=0 # cases with different anomalies
	
	failed=0 # no reports found
	def __init__(self):
		return

class Report(object):
	full_report=''
	file_name=''
	file_md5=''
	timedout=False 
	imports_list=[]
	dropped_list=[]
	host_list=[]
	dns_req=[]
	anom_list=[]
	file_list=[]
	mutex_list=[]
	regkey_list=[]
	proc_list=[]
	
	def __init__(self, full_report):
		self.full_report=full_report
		(self.file_name, self.file_md5)=self.loadFileDetails()
		self.imports_list=self.loadImports()
		self.dropped_list=self.loadDroppedFiles()
		(self.host_list, self.dns_req)=self.loadNetwork()
		(self.file_list, self.mutex_list, self.regkey_list, self.anom_list)=self.loadBehavior()
		self.proc_list=self.loadProcesses()
		#Timeout
		try:
			re.search('The analysis hit the critical timeout', full_report).group()
			self.timedout=True
		except:
			self.timedout=False
			
		return
		
	def loadFileDetails(self):
		sub_1=secciona(self.full_report, '<section id="file">', '</section>')
		file_name=secciona(sub_1, '<th>File name</th>', '</span></td>').split('>')[-1]
		file_md5=secciona(sub_1, '<th>MD5</th>', '</span></td>').split('>')[-1]		
		return (file_name, file_md5)		
	def loadImports(self):
		imp_list=[]
		sub_1=secciona(self.full_report, ">Imports</a></h4>",">Strings</a></h4>")
		libraries=sub_1.split('<div class="well">')[1:]
		for lib in libraries:
			function_list=[]
			library_name=secciona(lib, 'Library', '</strong>:</div>')
			func=lib.split('<div>&bull;')[1:]
			for fu in func:
				function_list.append(secciona(fu, '</span> - ', '</div>'))
			imp_list.append([library_name, function_list])
		return imp_list	
	def loadDroppedFiles(self):
		file_list=[]
		sub_1=secciona(self.full_report, '<section id="dropped">', '</section>')
		files=sub_1.split('<table')[1:]
		for f in files:
			file_name=secciona(f, '<th>File name</th>', '</span></td>').split('>')[-1]
			md5=secciona(f, '<th>MD5</th>', '</span></td>').split('>')[-1]
			size=secciona(f, '<th>File size</th>', '</span></td>').split('>')[-1]
			_type=secciona(f, '<th>File type</th>', '</span></td>').split('>')[-1]
			file_list.append([file_name, md5, size, _type])
		return file_list
	def loadNetwork(self):
		trusted_names=["microsoft.com",
						"facebook.com",
						"akamaihd.net",
						"s-microsoft.com",
						"html5shim.googlecode.com",
						"googletagservices.com",
						"googleadservices.com",
						"fbcdn.net",
						"live.com",
						"google.es",
						"gstatic.com",
						"youtube.com",
						"youtube.es",
						"googleapis.com",
						"google-analytics.com",
						"googlesyndication.com"]
		_in=False
		host_list=[]
		dns_req=[]
		sub=secciona(self.full_report, '<section id="network">', '</section>')
		#Hosts
		sub_hosts=secciona(sub, '>Hosts Involved<', '</table>').split('<td><span class="mono">')[1:]
		for s in sub_hosts:
			host_list.append(s.split('<')[0])		
		#DNS
		sub_dns=secciona(sub, '>DNS Requests<', '</table>').split('<tr>')[2:]
		for s in sub_dns:
			name=s.split('<td><span class="mono">')[1].split('<')[0]
			ip=s.split('<td><span class="mono">')[2].split('<')[0]
			#Avoiding trusted sources
			for n in trusted_names:
				try:
					re.search(n, name).group()
					host_list.remove(ip)
					_in=True
				except:
					pass
			if not _in:
				dns_req.append([name, ip])
			_in=False
					
		return host_list, dns_req				
	def loadBehavior(self):
		file_list=[]
		mutex_list=[]
		regkey_list=[]
		anom_list=[]
		sub=secciona(self.full_report, '<section id="behavior">', '</section>')
		#Anomalies
		sub_an=secciona(sub, 'Anomalies', '</ul>').split('<li>')[1:]
		for s in sub_an:
			anom_list.append(secciona(s, '<b>', '</b>'))
		#Files
		sub_fi=secciona(sub, '<b>Files</b>',  '</ul>').split('<li>')[1:]
		for s in sub_fi:
			file_list.append(secciona(s, '<span class="mono">', '</span></li>'))
		#Mutex
		sub_mu=secciona(sub, '<b>Mutexes</b>',  '</ul>').split('<li>')[1:]
		for s in sub_mu:
			mutex_list.append(secciona(s, '<span class="mono">', '</span></li>'))
		#Registry keys
		sub_rk=secciona(sub, '<b>Registry Keys</b>',  '</ul>').split('<li>')[1:]
		for s in sub_rk:
			regkey_list.append(secciona(s, '<span class="mono">', '</span></li>'))				
		return file_list, mutex_list, regkey_list, anom_list		
	def loadProcesses(self):
		proc_list=[]
		sub=secciona(self.full_report, '<h4>Processes</h4>', '</section>')
		sub_p=sub.split('javascript:showHide')[1:]
		for s in sub_p:
			proc_list.append(s.split('>')[1][:-3])
		
		return proc_list	
		
	def __del__(self):
		
		return
		
def secciona(text, flag_1, flag_2):
		try:
			start=re.search(flag_1,text).span()[1]
		except:
			return ''
		try:
			end=re.search(flag_2,text[start:]).span()[0]
		except:
			return ''
		return text[start:][:end]

def compareRep(rep_1, rep_2, out_file, sta):
	# Directly
	sta.total_comps+=1
	# one of the reports hitted the time-out
	timed_out_bool=False 	
	#Statistics of the case
	no_drop=False
	timed_out=False
	anomalies=False
	equal_files=0
	new_files=0
	same_name_small=0
	same_name_big=0
	diff_type=0
	# statist bools
	has_drop=False

	shown=False
	file_found=False
	
	_in=False
	
	_f=open(out_file, 'w')	
	#Name
	_f.write("NAME\n########")
	if rep_1.file_name!=rep_2.file_name:
		_f.write("\n- Difference!: File name\n\t"+ rep_1.file_name+" - "+ rep_2.file_name)
	#MD5
	_f.write("\nMD5\n########")
	if rep_1.file_md5!=rep_2.file_md5:
		_f.write("\n- Difference!: File MD5\n\t"+ rep_1.file_md5+" - "+ rep_2.file_md5)
	#Timeout
	_f.write("\nTime-out\n########")
	if rep_1.timedout:
		_f.write('\n- Hardened analysis timed-out!\n')
		timed_out+=1
		timed_out_bool=True
	if rep_2.timedout:
		_f.write('\n- Raw analysis timed-out!\n')	
		timed_out+=1
		timed_out_bool=True
	#Rest of the comparision	
	if not timed_out_bool:	
		#Imports
		_f.write("\nIMPORTS\n########")
		for lib1, func_list1 in rep_1.imports_list:
			_in=False
			for lib2, func_list2 in rep_2.imports_list:
				if lib1==lib2:
					_in=True
					dif_set=set(func_list1).difference(func_list2)
					difs=len(dif_set)
					for i in range(difs):
						_f.write("\n- Difference!:\n\tLib "+lib1+" - Function "+dif_set.pop())
			if not _in:
				_f.write("\n- Difference!:\n\tLib "+lib1+" - All funcs.")						
		#Dropped files
		_f.write("\nDROPPED\n########")	
		for f1, md5_1, size1, _type1 in rep_1.dropped_list:
			# If there are no files, it does not enter the for
			has_drop=True 			
			shown=False
			for f2, md5_2, size2, _type2  in rep_2.dropped_list:
				if f1==f2: # same name
					file_found=True # file found in the second report										
					# Different size								
					if size1!=size2:
						_f.write("\n- Difference!:\n\tSize of "+f1+" hardened "+size1+", raw "+size2)
						# Files with less than 100 bytes of diference
						if abs(int(size1[:-6])-int(size2[:-6]))<100: 
							same_name_small+=1
						# Files with more than 100 bytes of diference
						else: 
							same_name_big+=1						
						shown=True						
					# Different type
					if _type1!=_type2:
						_f.write("\n- Difference!:\n\t type of "+f1+" hardened "+_type1+", raw "+_type2)				
						diff_type+=1
						shown=True				
					# Same fiele = same name, same type, same size
					if not shown:
						_f.write("\n- Same file!:\n\t "+f1)		
						equal_files+=1		
			if not file_found:
				_f.write("\n- Difference!:\n\tNew "+f1)
				new_files+=1		
															
		if not has_drop:
			no_drop=True										
		
		#Anomalies
		shown=False
		_f.write("\nANOMALIES\n########\n")	
		anom_1=set(rep_1.anom_list)
		anom_2=set(rep_2.anom_list)
		dif_set=anom_1.difference(anom_2)
		difs=len(dif_set)
		for i in range(difs):
			_f.write("\n- Difference!:\n\t"+dif_set.pop())
			if not shown:
				sta.anomalies+=1
						
		#Host
		_f.write("\nHOSTS\n########")	
		hosts_1=set(rep_1.host_list)
		hosts_2=set(rep_2.host_list)
		dif_set=hosts_1.difference(hosts_2)
		difs=len(dif_set)
		for i in range(difs):
			_f.write("\n- Difference!:\n\t"+dif_set.pop())
			
		"""
		#Opened files
		_f.write("\n\nOP FILES\n########\n")	
		anom_1=set(rep_1.file_list)
		anom_2=set(rep_2.file_list)
		dif_set=anom_1.difference(anom_2)
		difs=len(dif_set)
		for i in range(difs):
			_f.write("\n- Difference!:\n\t"+dif_set.pop())	
		#Mutexes
		_f.write("\n\nMUTEXES\n########\n")	
		anom_1=set(rep_1.mutex_list)
		anom_2=set(rep_2.mutex_list)
		dif_set=anom_1.difference(anom_2)
		difs=len(dif_set)
		for i in range(difs):
			_f.write("\n- Difference!:\n\t"+dif_set.pop())	
		#Reg. keys
		_f.write("\n\nREG KEYS\n########\n")	
		anom_1=set(rep_1.regkey_list)
		anom_2=set(rep_2.regkey_list)
		dif_set=anom_1.difference(anom_2)
		difs=len(dif_set)
		for i in range(difs):
			_f.write("\n- Difference!:\n\t"+dif_set.pop())		
		#Processes
		_f.write("\n\nPROCESSES\n########\n")	
		anom_1=set(rep_1.proc_list)
		anom_2=set(rep_2.proc_list)
		dif_set=anom_1.difference(anom_2)
		difs=len(dif_set)
		for i in range(difs):
			_f.write("\n- Difference!:\n\t"+dif_set.pop())	
		"""
		_f.close()	
	
	# Estadisticas generales
	if timed_out_bool:
		sta.timedout+=1
	if no_drop:
		sta.no_dropped+=1
	if anomalies:
		sta.anomalies+=1
	if new_files>0:
		sta.new_files+=1
	else:
		if same_name_big>0:
			sta.similar_files+=1
		elif same_name_small>0:
			sta.less_similar_files+=1
		elif equal_files>0:
			sta.same_files+=1	
	if diff_type>0:
		sta.diff_types+=1
							
	return
	
def failedRep(path, reason):
	_f=open(path, 'w')
	_f.write('\n'+reason)
	_f.close()
	
	return	
	
def main():
	_st=Statist()
	
	results_folder='/media/cuckoo/Data/test/Result_comparisons'
	if not os.path.exists(results_folder):
		os.system('mkdir '+results_folder)
		
	modified_path='/media/cuckoo/Data/test/hardened/requirements/cuckoo/storage/analyses/'
	raw_path='/media/cuckoo/Data/test/raw/requirements/cuckoo/storage/analyses/'
		
	for n in range(99):
		ready=False
		out_path=results_folder+'/comp_'+str(n)+'.txt'
		print out_path
		# Hardened cuckoo
		report_name=modified_path+str(n)+'/reports/report.html'
		try:		
			_f=open(report_name, 'r')
			full_report=_f.read()
			_f.close()
			rep_mod=Report(full_report)
			
			ready=True
		except IOError:
			failedRep(out_path, 'FAIL: Hardened Cuckoo')
		# Raw Cuckoo
		report_name=raw_path+str(n)+'/reports/report.html'
		#####
		if n>=76:
			report_name=raw_path+str(n+1)+'/reports/report.html'
		######
		try:					
			_f=open(report_name, 'r')
			full_report=_f.read()
			_f.close()
			rep_raw=Report(full_report)				
		except IOError:
			failedRep(out_path, 'FAIL: Raw Cuckoo')
			ready=False
			
		# Compare
		if ready:
			compareRep(rep_mod, rep_raw, out_path, _st)	
			print 'OK'
		else:
			print 'Fail'	
			_st.failed+=1
		
	_f=open(results_folder+'/Statistics.txt', 'w')
	_f.write('Reports not found: '+str(_st.failed))
	_f.write('\n\nNumber of analysis: '+str(_st.total_comps))
	
	_f.write('\n\nCases timed-out: '+str(_st.timedout))	
	_f.write('\nCases with NO files: '+str(_st.no_dropped))
	_f.write('\nCases with new files: '+str(_st.new_files))
	_f.write('\nCases with exactly the same files: '+str(_st.same_files))
		
	_f.write('\n\nCases with files with same name and less than 100 bytes of difference: '+str(_st.similar_files))
	_f.write('\nCases with files with same name and more than 100 bytes of difference: '+str(_st.less_similar_files))
	
	_f.write('\n\nCases with different types: '+str(_st.diff_types))
	_f.write('\nCases with anomalies: '+str(_st.anomalies))	

	_f.close()
	return
	
main()
exit(0)	
