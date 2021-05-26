#!/bin/bash
if [ -z "$1" ]; then
    echo
    echo usage: $0 [network-interface]
    echo
    echo e.g. $0 enp5s0f0
    echo
    echo adjusts irg balance for NIC queues
    exit
fi
dev="$1"


ncpus=`nproc`
test "$ncpus" -gt 1 || exit 1
echo "CPUs: $ncpus"


echo "Existing irq affinity for $dev:"
for irq in `awk -F "[ :]" "/$dev/"'{print $2}' /proc/interrupts`
do
    awk "/$irq:/"'{printf "%s ", $NF}' /proc/interrupts
    cat /proc/irq/$irq/smp_affinity
done


n=0
for irq in `awk -F "[ :]" "/$dev/"'{print $2}' /proc/interrupts`
do
    f="/proc/irq/$irq/smp_affinity"
    test -r "$f" || continue
    cpu=$[$ncpus - ($n % $ncpus) - 1]
    if [ $cpu -ge 0 ]
            then
                mask=`printf %x $[2 ** $cpu]`
                echo "Assign SMP affinity: $dev queue $n, irq $irq, cpu $cpu, mask 0x$mask"
                echo "$mask" > "$f"
                let n+=1
    fi
done