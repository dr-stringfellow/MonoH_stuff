void dropBranches(){

    //Get old file, old tree and set top branch address
    TFile *oldfile = new TFile("monojet_final_full.root");
    TFile *newfile = new TFile("monojet_final.root","recreate");
    
    TIter next (oldfile->GetListOfKeys());
    TKey *key;
    while ((key = (TKey*)next())) {
        if (strstr(key->GetClassName(),"TTree")) {
            printf (" key : %s is a %s \n",key->GetName(),key->GetClassName());
            TTree *oldtree = (TTree*)oldfile->Get(key->GetName());
            oldtree->SetBranchStatus("*",0);
            oldtree->SetBranchStatus("met",1);
            oldtree->SetBranchStatus("jet1Pt",1);
            oldtree->SetBranchStatus("scaleMC_w",1);
            oldtree->SetBranchStatus("genBos_pt",1);
            TTree *newtree = oldtree->CloneTree();
            newtree->SetName(key->GetName());
            
        }   
    }


    newfile->Write();
    delete oldfile;
    delete newfile;
}
