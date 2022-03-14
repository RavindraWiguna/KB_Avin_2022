#anzay ngetest early rng, is it loopin?
from collections import Counter
import os

def generate_random_seq(seed, rangeScope):
    prev_seed = seed
    seen = Counter()
    isGenerating = True
    tseed = 0
    count = 0
    while isGenerating and seed > 3:
        count +=1
        if(seen[seed]>0):
            isGenerating = False
            break
        seen[seed]+=1
        prev_seed = seed
        seed*= seed #too fast sir
        seed = str(seed)
        tseed = len(seed)
        tseed //=2
        # print(seed)
        before_div = seed
        seed = seed[0:tseed] + seed[tseed+1: ]
        # print(seed)
        try:
            seed = int(seed)
            seed %=rangeScope
        except ValueError:
            print(f'prev seed before error: {prev_seed}| beforediv {before_div}')
            isGenerating = False
        
        
        # os.system("pause")
    return count


if __name__=="__main__":
    # try:
                                                    print(generate_random_seq(4813, 1000000))
    #     curMax = -1
    #     iMax = 0
    #     for i in range(10, 100000):
    #         chall = generate_random_seq(i, 1000000)
    #         if(chall > curMax):
    #             iMax = i
    #             curMax = chall
        
    #     print(f'{iMax}: {curMax}')
    # except KeyboardInterrupt:
    #     print("lah bosku")