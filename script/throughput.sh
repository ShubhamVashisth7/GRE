num_iterations=3
threads=(2 4 8 16 24 36) 
datasets=("covid" "libio" "genome" "osm")
index_techniques=("alexol" "btreeolc" "hot" "masstree" "xindex")

for dataset in "${datasets[@]}"
do
    for thread_num in "${threads[@]}"
    do
        for index_technique in "${index_techniques[@]}"
        do
            for ((i=1; i<=$num_iterations; i++))
            do
                echo "iteration: $i, dataset: $dataset, thread_num: $thread_num, index_technique: $index_technique"
                ./build/microbench \
                --keys_file=./datasets/$dataset \
                --keys_file_type={binary,text} \
                --read=1.0 --insert=0.0 \
                --operations_num=800000000 \
                --table_size=-1 \
                --init_table_ratio=1.0 \
                --thread_num=$thread_num \
                --index=$index_technique
            done
        done
    done
done

