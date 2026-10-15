function visEvap(p,q,t)
    ylab = {'F200','P100','F3','L2','P2','X2'};
    sb = [1 3 5 2 4 6];
        
    if isempty(q)
        for j = 1:6
            subplot(3,2,sb(j)); plot(t,p(:,j),'b'); grid on;
            axis tight; ylabel(ylab{j});
        end
    else
        for j = 1:6
            subplot(3,2,sb(j)); plot(t,p(:,j),'b'); 
            hold on; plot(t,q(:,j),'r'); grid on;
            axis tight; ylabel(ylab{j});
        end
    end
end