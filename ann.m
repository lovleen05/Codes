fid = fopen('kddcup.data_10_percent_corrected','rt');
data = textscan(fid,['%f %s %s %s ', repmat('%f ',1,37), '%s'], 'delimiter',',');
fclose(fid); % load the data from kddcup in the form of cell
[~,~,data2]=unique(data{1,2});
data{1,2}=data2;
[~,~,data3]=unique(data{1,3});
data{1,3}=data3;
[~,~,data4]=unique(data{1,4});
data{1,4}=data4; % converting char to no
[~,~,data42]=unique(data{1,42});
data{1,42}=data42;

data_mat=cell2mat(data);% converting cells to matrix
unique_data=unique (data_mat,'rows'); % remove repeat inputs
var_data=var(unique_data);
idx=[];
for i = 1:41
    if var(unique_data(:,i))==0
        idx=[idx,i];
    end
end
p=unique_data; % remove the columns in which the value are same
 p(:,idx)=[];
normalised=zeros(size(p));
for n = 1:40 % normalizing the data
range = max(p(:,n)) - min(p(:,n));
normalised(:,n)=(p(:,n)-min(p(:,n)))/range;
end
%correlation above 0.6 and display them (in idx) and tells which of the 2 displayed
%columns have smaller variance so we can choose it to delete it later. At
%the end we will have a new normalized data table.
m=length(normalised(1,:))-1;
newnormdata=normalised;
limit=0.6;
idx=[];
for i=1:m
    for j=i:m
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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
newvar2=1000*var(newnormdata);
idx=[];
for i=1:length(newvar2)-2
    if newvar2(i)<=2
        idx=[idx;i];
    end
end
newnormdata(:,idx)=[];
newvar3 = 1000*var(newnormdata);
data_corr=corrcoef(normalised(:,1:40))
[coeff,score,latent,tsquared,explained,mu]=pca(newnormdata(:,1:end-1));



% for deleting the columns from the score based on explained .
% score(:,10:end)=[];
output=newnormdata(:,end);
target=zeros(size(output));
for i=1:length(output)
    if output(i)==0.5000
        target(i)=0;
    else
        target(i)=1;
    end
end