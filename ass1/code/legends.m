% Scientific Visualization and Virtual Reality
% Assignment 1

figure;
hold on;

plot(.5,.5,'ro')
plot(1,1,'go')
plot(1.5,1.5,'bo')


%plot(.5,.5,'w^')
%plot(1,1,'ws')
%plot(1.5,1.5,'wp')
%plot(1,1,'whh')
%plot(1.5,1.5,'wo')
%plot(1,1,'wd')

whitebg([0 .5 .6])

%legend({'3','4', '5','6', '7', '8'},'FontSize',8,'FontWeight','bold')
%hleg = legend('3','4', '5','6', '7', '8','FontSize',12,'FontWeight','bold');
%htitle = get(hleg,'Title');
%set(htitle,'String','Cylinders')

hleg = legend('US','Japan', 'Europe','FontSize',12,'FontWeight','bold');
htitle = get(hleg,'Title');
set(htitle,'String','Origin')


hold off;
