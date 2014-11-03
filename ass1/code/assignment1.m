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
grid on;

for i=1:200%392
    if strcmp(origin(i), 'US'); 
        color = ((year(i)-70)/15 + 0.2) * [1 0 0]; %red
        size = 100;
        scatter3(mpg(i), hp(i), weigth(i), size, color, 'filled')
    elseif strcmp(origin(i),'Japan');
        color = ((year(i)-70)/15 + 0.2) * [0 1 0]; %green
        size = 100;
        scatter3(mpg(i), hp(i), weigth(i), size, color, 'filled')
    elseif strcmp(origin(i),'Europe');
        color = ((year(i)-70)/15 + 0.2) * [0 0 1]; %blue
        size = 100;
        scatter3(mpg(i), hp(i), weigth(i), size, color, 'filled')
    end
end

xlabel('MPG')
ylabel('Horsepower')
zlabel('Weigth')
legend('US', 'Japan', 'Europe')

grid on;
grid;
hold off;
