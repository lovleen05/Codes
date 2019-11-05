fid = fopen('train','rt');

%%
train_mat=cell2mat(table2cell(train));
n_variables=length(train_mat(1,:))-1;% display the independent variables
n_samples=length(train_mat(:,1)); % shows the sample in verticle order
% check for NaN values
idx=[];
for i=1:n_variables+1
    for j=1:n_samples
        if isnan(train_mat(j,i))==1
            idx=[idx;[j,i]];
        end
    end
end
% remove constant columns
i=1;
while i<=n_variables
    if var(train_mat(:,i))==0
        train_mat(:,i)=[];
        n_variables=length(train_mat(1,:))-1;
    else
        i=i+1;
    end
end
    
normalised=zeros(size(train_mat));
for n = 1:n_variables+1 % normalizing the data
range = max(train_mat(:,n)) - min(train_mat(:,n));
normalised(:,n)=(train_mat(:,n)-mean(train_mat(:,n)))/sqrt(var(train_mat(:,n)));
end
%%
%variance
newvardata = var(normalised);
%var_data=var_data*1000
%%
%correlation
data_corr=corrcoef(normalised(:,1:n_variables))
%%
% column deleting
%looping in new var data table and then finding columns which have
%correlation above 0.6 and display them (in idx) and tells which of the 2 displayed
%columns have smaller variance so we can choose it to delete it later. At
%the end we will have a new normalized data table.
newnormdata=normalised;
limit=0.6;
idx=[];
for i=1:n_variables
    for j=i:n_variables
        if i==j
        elseif data_corr(i,j)>=limit
            if newvardata(i)>newvardata(j)
                idx=[idx;i,j,newvardata(j)];
            else
                idx=[idx;j,i,newvardata(i)];
            end
        end
    end
end
newnormdata(:,idx(:,2))=[];
%%
newvar2=1000*var(newnormdata);
idx=[];
for i=1:length(newvar2)-2
    if newvar2(i)<=2
        idx=[idx;i];
    end
end
newnormdata(:,idx)=[];
newvar3 = 1000*var(newnormdata);
%%
% pca
[coeff,score,latent,~,explained,mu]=pca(newnormdata(:,1:end-1));
% deleting columns based on explained values
sum_explained=cumsum(explained);
score_reduced=score;
for i=1:n_variables
    if sum_explained(i)>99
        score_reduced=score(:,1:i);
        break
    end
end

output=zeros(n_samples,3);
for i=1:n_samples
    if train_mat(i,end)==1
    elseif train_mat(i,end)==2
        output(i,3)=1;
    elseif train_mat(i,end)==3
        output(i,2)=1;
    elseif train_mat(i,end)==4
        output(i,2)=1;
        output(i,3)=1;
    elseif train_mat(i,end)==5
        output(i,1)=1;
    elseif train_mat(i,end)==6
        output(i,1)=1;
        output(i,3)=1; 
    elseif train_mat(i,end)==7
        output(i,1)=1;
        output(i,2)=1;
    end
end
