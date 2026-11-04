"""Deterministic alternating-bit teaching model. No network sockets or sleeps."""
import argparse,csv,heapq,itertools,json,sys

CASES=('no-loss','data-loss','ack-loss','combined-loss','delayed-ack')

def simulate(case):
    if case not in CASES:raise ValueError('Unknown case')
    events=[];counter=itertools.count();trace=[];delivered=[]
    messages=['ALPHA','BETA'];sender_index=0;expected=0;waiting=False;generation=0
    attempts={};ack_count={};data_transmissions=0;timeouts=0;duplicates=0;ignored_acks=0
    def schedule(t,kind,**fields):heapq.heappush(events,(t,next(counter),kind,fields))
    def log(t,actor,event,seq='',payload='',detail=''):
        trace.append(dict(step=len(trace)+1,time=t,actor=actor,event=event,sequence=seq,payload=payload,detail=detail,delivered_count=len(delivered)))
    def send(t):
        nonlocal generation,waiting,data_transmissions
        seq=sender_index%2;payload=messages[sender_index];waiting=True;generation+=1
        attempts[sender_index]=attempts.get(sender_index,0)+1;data_transmissions+=1
        log(t,'sender','send_DATA',seq,payload,'Start/restart the fixed logical timer')
        if case in ('data-loss','combined-loss') and sender_index==0 and attempts[0]==1:
            log(t,'channel','drop_DATA',seq,payload,'First DATA0 is lost in this case')
        else:schedule(t+1,'DATA',seq=seq,payload=payload)
        schedule(t+5,'TIMEOUT',generation=generation)
    send(0)
    while events and sender_index<len(messages):
        t,_,kind,fields=heapq.heappop(events)
        if t>100:raise RuntimeError('Teaching model did not terminate')
        if kind=='TIMEOUT':
            if not waiting or fields['generation']!=generation:continue
            timeouts+=1;log(t,'sender','timeout',sender_index%2,messages[sender_index],'No matching ACK received before the deadline');send(t)
        elif kind=='DATA':
            seq,payload=fields['seq'],fields['payload']
            log(t,'receiver','receive_DATA',seq,payload,'Expected sequence before processing: '+str(expected))
            if seq==expected:
                delivered.append(payload);expected=1-expected
                log(t,'receiver','deliver',seq,payload,'Deliver once; next expected sequence: '+str(expected))
            else:
                duplicates+=1;log(t,'receiver','suppress_duplicate',seq,payload,'Keep the application delivery list unchanged')
            ack_count[seq]=ack_count.get(seq,0)+1
            log(t,'receiver','send_ACK',seq,'','ACK identifies this DATA label')
            if case in ('ack-loss','combined-loss') and seq==0 and ack_count[seq]==1:
                log(t,'channel','drop_ACK',seq,'','First ACK0 is lost in this case')
            else:
                delay=7 if case=='delayed-ack' and seq==0 and ack_count[seq]==1 else 1
                if delay>1:log(t,'channel','delay_ACK',seq,'','First ACK0 takes 7 logical units to arrive')
                schedule(t+delay,'ACK',seq=seq)
        elif kind=='ACK':
            seq=fields['seq'];log(t,'sender','receive_ACK',seq,'','Current outstanding sequence: '+str(sender_index%2))
            if waiting and seq==sender_index%2:
                log(t,'sender','accept_ACK',seq,'','Advance to the next application message');waiting=False;sender_index+=1
                if sender_index<len(messages):send(t)
            else:
                ignored_acks+=1;log(t,'sender','ignore_ACK',seq,'','ACK does not match the outstanding message')
    if delivered!=messages:raise AssertionError('Delivery invariant failed')
    return dict(case=case,time_unit='logical, not seconds',trace=trace,delivered=delivered,data_transmissions=data_transmissions,timeouts=timeouts,duplicate_data=duplicates,ignored_acks=ignored_acks,completion_time=trace[-1]['time'])

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',choices=CASES,required=True);p.add_argument('--csv',help='Write a new trace CSV; existing files are preserved');p.add_argument('--json',action='store_true',help='Print machine-readable trace and summary');a=p.parse_args();r=simulate(a.case)
    if a.csv:
        try:
            with open(a.csv,'x',newline='',encoding='utf8')as f:
                writer=csv.DictWriter(f,fieldnames=list(r['trace'][0]));writer.writeheader();writer.writerows(r['trace'])
        except FileExistsError:p.error('Output already exists. Choose a new trace filename.')
    if a.json:print(json.dumps(r,indent=2));return
    print('SYNTHETIC MODEL - logical time units, no network traffic')
    print('Case:',a.case)
    for e in r['trace']:
        print(f"#{e['step']:02} t={e['time']:>2}  {e['actor']:<8} {e['event']:<20} seq={e['sequence']} {e['payload']} | {e['detail']} | deliveries={e['delivered_count']}")
    print('Delivered messages:',', '.join(r['delivered']))
    print('DATA transmissions:',r['data_transmissions'],'Timeouts:',r['timeouts'],'Duplicate DATA:',r['duplicate_data'],'Ignored ACKs:',r['ignored_acks'])
if __name__=='__main__':main()
