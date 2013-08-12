plohand
=======

PLO Hand Analysis tools
Code written by djsensei, with a kickstart from Ethan Leland

If you want to help out, let me know! Please don't take the code without asking, though. 

Eventual goals (in order):
1) An engine that will take in a PLO starting hand and analyze all the ways it interacts
   with boards, particularly how often it will make the nuts/2nd nuts/etc.
2) Run a bunch of random hands through the engine to determine relative frequencies of each
   type of interaction, and formulate percentile tables. 
   i.e. AKQJ is the 100% percentile for making top 2 pair, KK22ds is the 60% percentile for 
   making the nut flush, etc.
3) Develop a GUI that allows a user to input a hand and outputs all the frequencies/percentiles
   for the flop/turn/river. Ideally, the percentiles will be color-coded to aid in interpreting
   the results (red = 0%, green = 100%)
4) (Somewhat subjectively) determine a classifier system for hands that aids in preflop
   decision-making. i.e. a hand with high nuts % and high freeroll % is strong for high-SPR
   and/or multiway spots (limped pots!) while a hand with medium nuts % but high floppability
   is good for low-SPR heads-up spots (3bet to isolate!)