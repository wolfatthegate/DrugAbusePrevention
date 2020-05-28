## https://github.com/JiaShun-Xiao/BLAST-bioinfor-tool/blob/master/blast.py
# compare single base
import nltk
import pandas as pd

class blast:
    def SingleBaseCompare(self, char1,char2):
        if char1 == char2:
            return 2
        else:
            return -1
        
    def W2WCompare(self, word1, word2, threshold):
        result = blast.SMalignmentGlobal(self, word1.lower(), word2.lower())
        if result[2] > threshold:
            return 2
        else: 
            return -1
    
    def SMWalignment(self, seq1, seq2, threshold):
        
        seq1 = '~~ ' + seq1 + ' ~~'
        seq2 = '^^ ' + seq2 + ' ^^'
        
        seq1_tokens = nltk.word_tokenize(seq1)
        seq2_tokens = nltk.word_tokenize(seq2)
        
        if len(seq1_tokens) < 4 or len(seq2_tokens) < 4:
            return '', '', 0, 0
        
        m = seq1_tokens.__len__() - 1
        n = seq2_tokens.__len__() - 1
        g = -3
        
        matrix = []
        matchMap = []
        matchCounter = 0
        
        for i in range(0, m):
            tmp = []
            for j in range(0, n):
                tmp.append(0)
            matrix.append(tmp)
            
        for i in range(0, m):
            tmp = []
            for j in range(0, n):
                tmp.append(0)
            matchMap.append(tmp)
            
        for sii in range(0, m):
            matrix[sii][0] = sii*0
             
        for sjj in range(0, n):
            matrix[0][sjj] = sjj*0
        
        for siii in range(1, m):
            for sjjj in range(1, n):
                matchScore = blast.W2WCompare(self, seq1_tokens[siii], seq2_tokens[sjjj],threshold)
                
                leftCell = matrix[siii][sjjj-1] + g
                upperCell = matrix[siii-1][sjjj] + g
                cornerCell = matrix[siii - 1][sjjj - 1] + matchScore  
                     
                matrix[siii][sjjj] = max(leftCell, upperCell, cornerCell)
                              
                if matchScore is 2: 
                    matchMap[siii][sjjj] = 2
                    matchCounter += 1
                else:
                    matchMap[siii][sjjj] = 0
        
        if matchCounter is 0:
            return 'no match found', '', 0, 0
        
#         df = pd.DataFrame(matrix)
#         print(df)
        
        sequ1 = []
        sequ2 = []
        
        m = m - 1
        n = n - 1
        
        firstMatch = False
        
        while firstMatch == False:
            if m > 0 and n > 0:  
                if matchMap[m][n] is 2: 
                    sequ1.append(seq1_tokens[m] + ' ')
                    sequ2.append(seq2_tokens[n] + ' ')
                    firstMatch = True
                
                if max(matrix[m][n-1], matrix[m-1][n-1], matrix[m-1][n]) == matrix[m-1][n-1]:
                    m -= 1
                    n -= 1
                elif max(matrix[m][n-1], matrix[m-1][n-1], matrix[m-1][n]) == matrix[m][n-1]:
                    n -= 1
                else:
                    m -= 1
            else: 
                return '---not match found', '---', 0, 0
            
        while m > 0 and n > 0:
            if matchMap[m][n] is 2: 
                sequ1.append(seq1_tokens[m] + ' ')
                sequ2.append(seq2_tokens[n] + ' ')
                
            if max(matrix[m][n-1], matrix[m-1][n-1], matrix[m-1][n]) == matrix[m-1][n-1]:
                if matchMap[m][n] is not 2: 
                    sequ1.append(seq1_tokens[m] + ' ')
                    sequ2.append(blast.fillspace(self, len(seq1_tokens[m])) + ' ')              
                m -= 1
                n -= 1
                  
            elif max(matrix[m][n-1], matrix[m-1][n-1], matrix[m-1][n]) == matrix[m][n-1]:     
                sequ1.append(blast.fillspace(self, len(seq2_tokens[n-1])) + ' ')
                sequ2.append(seq2_tokens[n-1] + ' ')
                n -= 1
            else:               
                sequ1.append(seq1_tokens[m-1] + ' ')
                sequ2.append(blast.fillspace(self, len(seq1_tokens[m-1])) + ' ')
                m -= 1
                 
        sequ1.reverse()
        sequ2.reverse()
        
        align_seq1 = ''.join(sequ1)
        align_seq2 = ''.join(sequ2)
        align_counter = 0

        for k in range(0, len(sequ1)):
            if blast.W2WCompare(self, sequ1[k], sequ2[k], threshold) is 2:
                align_counter += 1
        align_score = float(align_counter)/len(sequ1)
        
        return align_seq1, align_seq2, align_score, align_counter
    
    # Smith–Waterman char Alignment 
    # Use this algorithm to implement 
    def SMalignmentLocal(self, seq1, seq2):
        
        # pad with starting and ending 
        seq1 = '~' + seq1 + '~'
        seq2 = '^' + seq2 + '^'
        
        m = len(seq1) - 1
        n = len(seq2) - 1
        g = -3
        matrix = []
        for i in range(0, m):
            tmp = []
            for j in range(0, n):
                tmp.append(0)
            matrix.append(tmp)
            
        for sii in range(0, m):
            matrix[sii][0] = sii*0
        for sjj in range(0, n):
            matrix[0][sjj] = sjj*0
            
        for siii in range(1, m):
            for sjjj in range(1, n):
                singleBaseScore = blast.SingleBaseCompare(self, seq1[siii],seq2[sjjj])
                currCellScore = matrix[siii - 1][sjjj - 1] + singleBaseScore
                # update the score of cell - siii, sjjj
                matrix[siii][sjjj] = max(matrix[siii-1][sjjj] + g, currCellScore, matrix[siii][sjjj-1] + g)
                
        df = pd.DataFrame(matrix)
        print(df)
        
        sequ1 = []
        sequ2 = []        

        m = m-1
        n = n-1
        firstMatch = False
        # find the first match
        
        while firstMatch == False: 
            if seq1[m] == seq2[n]: 
                sequ1.append(seq1[m])
                sequ2.append(seq2[n])
                firstMatch = True
            
            if max(matrix[m][n-1], matrix[m-1][n-1], matrix[m-1][n]) == matrix[m-1][n-1]:
                m -= 1
                n -= 1
            elif max(matrix[m][n-1], matrix[m-1][n-1], matrix[m-1][n]) == matrix[m][n-1]:
                n -= 1
            else:
                m -= 1
        
        while m > 0 or n > 0:
            if seq1[m] == seq2[n]: 
                sequ1.append(seq1[m])
                sequ2.append(seq2[n])
            if max(matrix[m][n-1], matrix[m-1][n-1], matrix[m-1][n]) == matrix[m-1][n-1]:
                m -= 1
                n -= 1
            elif max(matrix[m][n-1], matrix[m-1][n-1], matrix[m-1][n]) == matrix[m][n-1]:
                sequ1.append('-')
                sequ2.append(seq2[n-1])
                n -= 1
            else:
                sequ1.append(seq1[m-1])
                sequ2.append('-')
                m -= 1
        sequ1.reverse()
        sequ2.reverse()
        
        print(sequ1)
        print(sequ2)
        firstTime = True
        firstIndex = 0
        align_seq1 = ''.join(sequ1)
        align_seq2 = ''.join(sequ2)
        align_score = 0.
        for k in range(0, len(align_seq1)):
            if align_seq1[k] == align_seq2[k]:
                if firstTime == True:
                    firstIndex = k 
                    firstTime = False
                align_score += 1
        align_score = float(align_score)/len(align_seq1[firstIndex:])
        return align_seq1, align_seq2, align_score  
    
    # Smith–Waterman Alignment 
    # Use it for word to word comparison
    def SMalignmentGlobal(self, seq1, seq2):
        m = len(seq1)
        n = len(seq2)
        g = -3
        matrix = []
        for i in range(0, m):
            tmp = []
            for j in range(0, n):
                tmp.append(0)
            matrix.append(tmp)
        for sii in range(0, m):
            matrix[sii][0] = sii*g
        for sjj in range(0, n):
            matrix[0][sjj] = sjj*g
        for siii in range(1, m):
            for sjjj in range(1, n):
                upperCell = matrix[siii-1][sjjj] + g
                leftCell = matrix[siii][sjjj-1] + g
                cornerCell = matrix[siii - 1][sjjj - 1] + blast.SingleBaseCompare(self, seq1[siii],seq2[sjjj])
                matrix[siii][sjjj] = max(upperCell, leftCell, cornerCell)
        sequ1 = [seq1[m-1]]
        sequ2 = [seq2[n-1]]
        while m > 1 and n > 1:
            if max(matrix[m-1][n-2], matrix[m-2][n-2], matrix[m-2][n-1]) == matrix[m-2][n-2]:
                m -= 1
                n -= 1
                sequ1.append(seq1[m-1])
                sequ2.append(seq2[n-1])
            elif max(matrix[m-1][n-2], matrix[m-2][n-2], matrix[m-2][n-1]) == matrix[m-1][n-2]:
                n -= 1
                sequ1.append('-')
                sequ2.append(seq2[n-1])
            else:
                m -= 1
                sequ1.append(seq1[m-1])
                sequ2.append('-')
        sequ1.reverse()
        sequ2.reverse()
        align_seq1 = ''.join(sequ1)
        align_seq2 = ''.join(sequ2)
        align_score = 0.
        
        for k in range(0, len(align_seq1)):
            if align_seq1[k] == align_seq2[k]:
                align_score += 1
        align_score = float(align_score)/len(align_seq1)
        return align_seq1, align_seq2, align_score
    
    def fillspace(self, length):
        s = ''
        for x in range(0, length): 
            s = s + '-'
        return s
            
