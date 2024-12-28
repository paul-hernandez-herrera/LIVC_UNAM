function ID = get_TPID(currentTP)

if (currentTP<10)
    ID = ['TP000' num2str(currentTP)];
elseif (currentTP<100)
    ID = ['TP00' num2str(currentTP)];
elseif (currentTP<1000)
    ID = ['TP0' num2str(currentTP)];
elseif (currentTP<10000)
    ID = ['TP' num2str(currentTP)];    
end

end