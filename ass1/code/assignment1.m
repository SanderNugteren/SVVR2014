% Scientific Visualization and Virtual Reality
% Assignment 1

table = readtable('cars.csv');

% Nominal
model = table{:,{'model'}};
origin = table{:,{'origin'}};

% Quantity Interval
year = table{:,{'year'}};

% Quantity Ratio
cylinders = table{:,{'cylinders'}};
hp = table{:,{'horsepower'}};
mpg = table{:,{'MPG'}};
weigth = table{:,{'weigth'}};

figure;
hold on;


for i=1:392
    if cylinders(i) == 3;
        shape = '^';
    elseif cylinders(i) == 4;
        shape = 's';
    elseif cylinders(i) == 5;
        shape = 'p';
    elseif cylinders(i) == 6;
        shape = 'h';
    elseif cylinders(i) == 7;
        shape = 'o';
    elseif cylinders(i) == 8;
        shape = 'd';
    end
    
    if strcmp(origin(i), 'US'); 
        color = ((year(i)-70)/15 + 0.2) * [1 0 0]; %red
        size = 100;
        scatter3(mpg(i), hp(i), weigth(i), size, color, shape, 'filled', 'MarkerEdgeColor','r')
        %text(mpg(i), hp(i), weigth(i), model(i))
    elseif strcmp(origin(i),'Japan');
        color = ((year(i)-70)/15 + 0.2) * [0 1 0]; %green
        size = 100;
        scatter3(mpg(i), hp(i), weigth(i), size, color, shape, 'filled', 'MarkerEdgeColor','g')
    elseif strcmp(origin(i),'Europe');
        color = ((year(i)-70)/15 + 0.2) * [0 0 1]; %blue
        size = 100;
        scatter3(mpg(i), hp(i), weigth(i), size, color, shape, 'filled', 'MarkerEdgeColor','b')
    end
end
grid on;
xlabel('MPG', 'FontSize',20)
ylabel('Horsepower', 'FontSize',20)
zlabel('Weigth', 'FontSize',20)
whitebg([0 .5 .6])

%legend({'US','Japan', 'Europe'},'FontSize',8,'FontWeight','bold')
hold off;
