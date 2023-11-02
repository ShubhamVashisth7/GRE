num_iterations=3
threads=(36 24 16 8 4 2 1) 
datasets=("covid")
index_techniques=("alexol" "lippol" "xindex" "finedex" "artolc" "btreeolc" "masstree" "wormhole_u64")

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
                --keys_file_type=binary \
                --read=0.5 --insert=0.5 \
                --thread_num=$thread_num \
                --index=$index_technique
            done
        done
    done
done

