# SPARKY_backbone_assignment_assister
Assists in getting started with assigning the backbone using the HNCA and HNCACB peaklists. 

The program has 2 parts.

The first part will sort all backbone peaks into 3 categories. Peaks that ***only*** have i and i-1 peaks, peaks that have more than i and i-1 peaks (overlapping or nearby peaks), and peaks that only have i peaks (***for both ca and cb***). Thus 3 files are made for each category. 

The 2nd part then goes through every combination of ca and cb peaks ***only*** for peaks with i and i-1 (so 4 combinations), and attempts to find their match (thus, you can get both i+1 and i-1). Then you can easily search this table of matches by typing in the nitrogen co-ordinates from you nhsqc. 

There are 3 tolerances that can be varied. These define the range of values that are accepted (decreasing their value may exclude certain matches, but increasing it will create artificial matches). 


