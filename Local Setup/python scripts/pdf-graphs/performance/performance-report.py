import sys
from random import randint
from jtlParameters import *
from gcParameters import  *
from uptimeParameters import  *

import csv




def getNRandomeColors(n):
    colors = []
    for i in range(n):
        colors.append('%06X' % randint(0, 0xFFFFFF))

    return colors

def getIfHasAttribute(dictionary, key):
    if(key in list(dictionary.keys())):
        return dictionary[key]
    else:
        return "NA"


heap_sizes = ["100m", "200m"]
concurrent_users = [500, 1000]
message_sizes= [1024, 10240]
garbage_collectors= ["UseSerialGC", "UseG1GC"] #, "UseParallelGC" , "UseConcMarkSweepGC"

jtl_file_root = sys.argv[1]
gc_reports_root = sys.argv[2]
uptime_reports_root = sys.argv[3]
dashboard_files_root = sys.argv[4]
output_csv_file = sys.argv[5]



csv_file_records = []
headers = ['size', 'heap', 'user', 'collector', 'average_latency', 'min_latency', 'max_latency', 'percentile_90', 'percentile_95', 'percentile_99', 'throughput', 'error_rate',
                       'footprint', 'avgfootprintAfterFullGC', 'avgFreedMemoryByFullGC', 'avgfootprintAfterGC', 'avgFreedMemoryByGC',
                       'avgPause', 'minPause', 'maxPause', 'avgGCPause', 'avgFullGCPause', 'accumPause', 'fullGCPause',
                       'gcPause', 'gc_throughput', 'num_full_gc', 'num_minor_gc', 'freedMemoryPerMin', 'gcPerformance','fullGCPerformance',
                       'last_one_minutes_la', 'last_five_minutes_la', 'last_fifteen_minutes_la']
csv_file_records.append(headers)



for size in message_sizes:
    for heap in heap_sizes:
        for user in concurrent_users:
            for collector in garbage_collectors:
                jtl_file_name = jtl_file_root+"/"+str(user)+"_users/"+heap+"_heap/"+collector+"_collector/"+str(size)+"_message/results-measurement.jtl"
                gc_log_name = gc_reports_root+"/"+heap+"_Heap_"+str(user)+"_Users_"+collector+"_collector_" +str(size)+"_size_GCReport.csv"
                uptime_file_name = uptime_reports_root+"/uptime_dir/"+heap+"_Heap_"+str(user)+"_Users_"+collector+"_collector_" +str(size)+"_size_uptime.txt"
                dashboard_file_name = dashboard_files_root+"/"+str(user)+"_users/"+heap+"_heap/"+collector+"_collector/"+str(size)+"_message/content/js/dashboard.js"

                jtl_stat = readDashboard(dashboard_file_name)

                # jtl_stat["error"] = stat_table[5].strip()
                # jtl_stat["average"] = stat_table[6].strip()
                # jtl_stat["min"] = stat_table[7].strip()
                # jtl_stat["max"] = stat_table[8].strip()
                # jtl_stat["percentile_90"] = stat_table[9].strip()
                # jtl_stat["percentile_95"] = stat_table[10].strip()
                # jtl_stat["percentile_99"] = stat_table[11].strip()
                # jtl_stat["throughput"] = stat_table[12].strip()

                #latencies  = getLatencies(jtl_file_name)



                average_latency = jtl_stat["average"]
                min_latency = jtl_stat["min"]
                max_latency = jtl_stat["max"]
                percentile_90= jtl_stat["percentile_90"]
                percentile_95 = jtl_stat["percentile_95"]
                percentile_99 = jtl_stat["percentile_99"]
                throughput = jtl_stat["throughput"]
                error_rate = jtl_stat["error"]


                gc_parameters = readGCfile(gc_log_name)

                footprint  = getIfHasAttribute(gc_parameters, "footprint")

                avgfootprintAfterFullGC = getIfHasAttribute(gc_parameters, "avgfootprintAfterFullGC")

                avgFreedMemoryByFullGC = getIfHasAttribute(gc_parameters, "avgFreedMemoryByFullGC")

                avgfootprintAfterGC = getIfHasAttribute(gc_parameters, "avgfootprintAfterGC")

                avgFreedMemoryByGC = getIfHasAttribute(gc_parameters, "avgFreedMemoryByGC")

                avgPause = getIfHasAttribute(gc_parameters, "avgPause")

                minPause = getIfHasAttribute(gc_parameters, "minPause")

                maxPause = getIfHasAttribute(gc_parameters, "maxPause")

                avgGCPause = getIfHasAttribute(gc_parameters, "avgGCPause")

                avgFullGCPause = getIfHasAttribute(gc_parameters, "avgFullGCPause")

                accumPause = getIfHasAttribute(gc_parameters, "accumPause")

                fullGCPause = getIfHasAttribute(gc_parameters, "fullGCPause")

                gcPause = getIfHasAttribute(gc_parameters, "gcPause")

                gc_throughput = getIfHasAttribute(gc_parameters, "throughput")

                num_full_gc = getIfHasAttribute(gc_parameters, "Number of full GC")

                num_minor_gc = getIfHasAttribute(gc_parameters, "Number of Minor GC")

                freedMemoryPerMin = getIfHasAttribute(gc_parameters, "freedMemoryPerMin")

                gcPerformance = getIfHasAttribute(gc_parameters, "gcPerformance")

                fullGCPerformance = getIfHasAttribute(gc_parameters, "fullGCPerformance")




                load_averages = getLoadAverages(uptime_file_name)
                last_one_minutes_la = load_averages[1]
                last_five_minutes_la = load_averages[5]
                last_fifteen_minutes_la = load_averages[15]

                row = [size, heap, user, collector, average_latency, min_latency, max_latency, percentile_90, percentile_95, percentile_99, throughput, error_rate,
                       footprint, avgfootprintAfterFullGC, avgFreedMemoryByFullGC, avgfootprintAfterGC, avgFreedMemoryByGC,
                       avgPause, minPause, maxPause, avgGCPause, avgFullGCPause, accumPause, fullGCPause,
                       gcPause, gc_throughput, num_full_gc, num_minor_gc, freedMemoryPerMin, gcPerformance,fullGCPerformance,
                       last_one_minutes_la, last_five_minutes_la, last_fifteen_minutes_la]
                csv_file_records.append(row)

with open(output_csv_file, "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in csv_file_records:
        writer.writerow(line)







