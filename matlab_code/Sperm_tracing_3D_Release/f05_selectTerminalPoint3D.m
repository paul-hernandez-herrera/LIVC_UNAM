function varargout = f05_selectTerminalPoint3D(varargin)
% F05_SELECTTERMINALPOINT3D MATLAB code for f05_selectTerminalPoint3D.fig
%      F05_SELECTTERMINALPOINT3D, by itself, creates a new F05_SELECTTERMINALPOINT3D or raises the existing
%      singleton*.
%
%      H = F05_SELECTTERMINALPOINT3D returns the handle to a new F05_SELECTTERMINALPOINT3D or the handle to
%      the existing singleton*.
%
%      F05_SELECTTERMINALPOINT3D('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in F05_SELECTTERMINALPOINT3D.M with the given input arguments.
%
%      F05_SELECTTERMINALPOINT3D('Property','Value',...) creates a new F05_SELECTTERMINALPOINT3D or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before f05_selectTerminalPoint3D_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to f05_selectTerminalPoint3D_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help f05_selectTerminalPoint3D

% Last Modified by GUIDE v2.5 28-Jul-2021 21:05:54

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @f05_selectTerminalPoint3D_OpeningFcn, ...
                   'gui_OutputFcn',  @f05_selectTerminalPoint3D_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT

function stack_name_prefix = get_stackName(stack_name_prefix,TP)

% ID = get_TPID2(TP);
ID = get_TPID(TP);

stack_name_prefix = [stack_name_prefix '_' ID '_DC'];


% --- Executes just before f05_selectTerminalPoint3D is made visible.
function f05_selectTerminalPoint3D_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to f05_selectTerminalPoint3D (see VARARGIN)
% close all;
% clear all;
% NOTA DE IAN: Aqui vas a poner la ruta donde esta la base de datos
handles.folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp17_stacks\stacks_constant_sampling';
% NOTA DE IAN: Aqui pones el nombre del conjunto, en este caso Exp7_stacks
handles.stack_name_prefix = 'Exp17_stacks';
% NOTA DE IAN: Aqui pones el fotograma en el que vas a iniciar la seleccion
handles.TP_initial = 1;
% NOTA DE IAN: Aqui pones el fotograma en el que vas a temrinar la
% seleccion, la base de datos que tenemos tiene hasta el 312, pero tu
% puedes elejir el 50 por ejemplo
handles.TP_final = 273;
% NOTA DE IAN: El codigo te genera un archivo donde vienen las coordenadas
% de la seleccion que hiciste en la carpeta donde la base de datos

k = 1;
while exist(fullfile(handles.folder_path,[handles.stack_name_prefix '_endPoints_' num2str(k) '.mat']),'file')
    k=k+1;
end
handles.file_mat_output = [handles.stack_name_prefix '_endPoints_' num2str(k) '.mat'];

handles.TP = handles.TP_initial;
handles.current_name = get_stackName(handles.stack_name_prefix,handles.TP);

for i=handles.TP_initial: handles.TP_final
    handles.traslation{i}=[];
    handles.min_x{i}=[];
    handles.min_y{i}=[];
    handles.min_z{i}=[];
    handles.Z_slice{i} = [];
end

V = readStack(handles.folder_path,handles.current_name);

displayProjections(V,[],handles);

set(handles.Previousbutton,'Enable','off') 

% Choose default command line output for f05_selectTerminalPoint3D
handles.output = hObject;

% set( gcf, 'toolbar', 'figure' )

% Update handles structure
guidata(hObject, handles);

function [min_x, min_y, min_z]=displayProjections(V,center,handles)
w_size = str2num(get( handles.edit1, 'String' ));
if isempty(center)
    center = [1 1 1];
    w_size = 10000;
end
x = center(1); y = center(2); z=center(3);

set(gcf,'name',['GUI - TP ' num2str(handles.TP) ])
min_x = x-w_size;
max_x = x+w_size;
min_y = y-w_size;
max_y = y+w_size;
min_z = z-w_size;
max_z = z+w_size;

if min_x<1
    min_x=1;
end
if min_y<1
    min_y=1;
end
if min_z<1
    min_z=1;
end
if max_x >size(V,1)
    max_x = size(V,1);
end
if max_y >size(V,2)
    max_y = size(V,2);
end
if max_z >size(V,3)
    max_z = size(V,3);
end

V = V(min_x:max_x,min_y:max_y,min_z:max_z);
% V = 255-V;
% hold all
% h=imshow(max(V,[],3)',[],'Parent', handles.axes1); 


h=imshow(get_image_to_show(V),[],'Parent', handles.axes1); 
set(h,'ButtonDownFcn',{@pickedXY,handles});
% set (gcf, 'WindowScrollWheelFcn', @mouseScroll);
% colormap(gca,jet)

I = V==0;
V(I) = mean(V(~I));
% V(I) = 255;

im_proYZ = max(V,[],1); im_proYZ=reshape(im_proYZ,[size(im_proYZ,2) size(im_proYZ,3)])';
im_proYZ = im_proYZ(end:-1:1,:);
h=imshow(im_proYZ,[],'Parent', handles.axes2);title('YZ','Parent', handles.axes2);colormap('gray')
set(h,'ButtonDownFcn',{@pickedYZ,handles});
% colormap(gca,jet)
% 
reSampleFactor=3;
im_proXZ = max(V,[],2); im_proXZ=reshape(im_proXZ,[size(im_proXZ,1) size(im_proXZ,3)])';
im_proXZ = im_proXZ(end:-1:1,:);
im_proXZ = imresize(im_proXZ,[reSampleFactor*size(im_proXZ,1) size(im_proXZ,2)]) ;
h=imshow(im_proXZ,[],'Parent', handles.axes3);title('XZ','Parent', handles.axes3)
set(h,'ButtonDownFcn',{@pickedXZ,handles});
colormap(gca,gray)

track= [];
for i=-5:0
    if (handles.TP+i)>0
        if not(isempty(handles.traslation{handles.TP+i}))
            if i==0
                save(fullfile(handles.folder_path,handles.file_mat_output),'-struct','handles','x_SP','y_SP','z_SP');
                colorid = 'g*';
            else
                colorid = 'r*';
            end
            track = [track; handles.x_SP{handles.TP+i}-min_x+1, handles.y_SP{handles.TP+i} - min_y+1];
            axes(handles.axes1);
            hold on;
            plot(handles.x_SP{handles.TP+i}-min_x+1, handles.y_SP{handles.TP+i} - min_y+1, colorid)
            hold off;

            axes(handles.axes2);
            hold on;
            plot(handles.y_SP{handles.TP+i} - min_y+1,size(V,3) - (handles.z_SP{handles.TP+i}- min_z+1), colorid)
            hold off;

            axes(handles.axes3);
            hold on;
            plot( handles.x_SP{handles.TP+i} - min_x +1,3*(size(V,3) - (handles.z_SP{handles.TP+i}- min_z+1)),colorid)
            hold off;
        end
    end   
end
if not(isempty(track))
    axes(handles.axes1);
    hold on;
    plot(track(:,1), track(:,2), 'r')
    hold off;
end

function [] = mouseScroll(hObject, eventdata, handles)
    UPDN = eventdata.VerticalScrollCount;
    
    handles = guidata(hObject);
    if not(isempty(handles.traslation{handles.TP}))
        handles.traslation{handles.TP} = [handles.min_x{handles.TP}-1 handles.min_y{handles.TP}-1 handles.min_z{handles.TP}-1];
    else
        handles.traslation{handles.TP} = [0,0,0];
    end
    handles.V{handles.TP}  = readStack(handles.folder_path,handles.current_name);
    
    if isempty(handles.z_SP{handles.TP})
        
        if (handles.TP > handles.TP_initial)
            if (not(isempty(handles.z_SP{handles.TP-1})))
                handles.z_SP{handles.TP} = handles.z_SP{handles.TP-1};
            end
        end
    else
        handles.z_SP{handles.TP} = handles.z_SP{handles.TP}-UPDN;
        if (handles.z_SP{handles.TP}>size(handles.V{handles.TP},3))
            handles.z_SP{handles.TP} = size(handles.V{handles.TP},3);
        elseif (handles.z_SP{handles.TP}<1)
            handles.z_SP{handles.TP} = 1;
        end
    end
    
    w_size = str2num(get( handles.edit1, 'String' ));
    
    
    
    if isempty(handles.x_SP{handles.TP})
        center = [1 1 1];
        w_size = 10000;
    else
        center = [handles.x_SP{handles.TP} handles.y_SP{handles.TP} handles.z_SP{handles.TP}];
    end
    x = center(1); y = center(2); z=center(3);

    set(gcf,'name',['GUI - TP ' num2str(handles.TP) ])
    min_x = x-w_size;
    max_x = x+w_size;
    min_y = y-w_size;
    max_y = y+w_size;
    min_z = z-w_size;
    max_z = z+w_size;

    V = handles.V{handles.TP} ;
    if min_x<1
        min_x=1;
    end
    if min_y<1
        min_y=1;
    end
    if min_z<1
        min_z=1;
    end
    if max_x >size(V,1)
        max_x = size(V,1);
    end
    if max_y >size(V,2)
        max_y = size(V,2);
    end
    if max_z >size(V,3)
        max_z = size(V,3);
    end

    V = handles.V{handles.TP}(min_x:max_x,min_y:max_y,handles.z_SP{handles.TP});

    h=imshow(get_image_to_show(V),[],'Parent', handles.axes1); 
    set(h,'ButtonDownFcn',{@pickedXY,handles});
    set (gcf, 'WindowScrollWheelFcn', @mouseScroll);
    
    guidata(handles.figure_selectTP3D,handles);  
    
 

    
    

function [] = pickedXY(hObject, eventdata, handles)
handles = guidata(hObject);
if not(isempty(handles.traslation{handles.TP}))
    handles.traslation{handles.TP} = [handles.min_x{handles.TP}-1 handles.min_y{handles.TP}-1 handles.min_z{handles.TP}-1];
else
    handles.traslation{handles.TP} = [0,0,0];
end
a = get(gca,'CurrentPoint' );
x = a(1,1);
y = a(1,2);
handles.x_SP{handles.TP} = round(mean(x)) + handles.traslation{handles.TP}(1); center(1)= handles.x_SP{handles.TP};
handles.y_SP{handles.TP} = round(mean(y)) + handles.traslation{handles.TP}(2); center(2)= handles.y_SP{handles.TP};
if isfield(handles,'z_SP')
    if length(handles.z_SP)>=handles.TP
        if isempty(handles.z_SP{handles.TP})
            handles.z_SP{handles.TP} = 0; 
            handles.min_z{handles.TP} = 0; 
        end
    else
        handles.z_SP{handles.TP} = 0; 
        handles.min_z{handles.TP} = 0;             
    end
else
    handles.z_SP{handles.TP} = 0; 
    handles.min_z{handles.TP} = 0;             
end

center(3)= handles.z_SP{handles.TP};
%         center

V = readStack(handles.folder_path,handles.current_name);
[handles.min_x{handles.TP}, handles.min_y{handles.TP}, handles.min_z{handles.TP}]=displayProjections(V,center,handles);
guidata(handles.figure_selectTP3D,handles);  
% a = get(gca,'CurrentPoint' );
% text(a(1,1),a(1,2),'A');
     
function [] = pickedYZ(hObject, eventdata, handles)
handles = guidata(hObject);
V = readStack(handles.folder_path,handles.current_name);
if not(isempty(handles.traslation{handles.TP}))
    handles.traslation{handles.TP} = [handles.min_x{handles.TP}-1 handles.min_y{handles.TP}-1 handles.min_z{handles.TP}-1];
else
    handles.traslation{handles.TP} = [0,0,0];
end
a = get(gca,'CurrentPoint' );
y = a(1,1);
z = a(1,2);
handles.z_SP{handles.TP} = size(V,3) - (round(mean(z)) + handles.traslation{handles.TP}(3))+1; center(3)= handles.z_SP{handles.TP};
handles.y_SP{handles.TP} = round(mean(y)) + handles.traslation{handles.TP}(2); center(2)= handles.y_SP{handles.TP};
if isfield(handles,'x_SP')
    if length(handles.x_SP)>=handles.TP
        if isempty(handles.x_SP{handles.TP})
            handles.x_SP{handles.TP} = 0; 
            handles.min_x{handles.TP} = 0; 
        end
    else
        handles.x_SP{handles.TP} = 0; 
        handles.min_x{handles.TP} = 0;             
    end
else
    handles.x_SP{handles.TP} = 0; 
    handles.min_x{handles.TP} = 0;             
end

center(1)= handles.x_SP{handles.TP};
%         center


[handles.min_x{handles.TP}, handles.min_y{handles.TP}, handles.min_z{handles.TP}]=displayProjections(V,center,handles);
guidata(handles.figure_selectTP3D,handles); 

function [] = pickedXZ(hObject, eventdata, handles)
handles = guidata(hObject);
V = readStack(handles.folder_path,handles.current_name);
if not(isempty(handles.traslation{handles.TP}))
    handles.traslation{handles.TP} = [handles.min_x{handles.TP}-1 handles.min_y{handles.TP}-1 handles.min_z{handles.TP}-1];
else
    handles.traslation{handles.TP} = [0,0,0];
end
a = get(gca,'CurrentPoint' );
x = a(1,1);
z = a(1,2);
handles.z_SP{handles.TP} = size(V,3) - (round(mean(z)/3) + handles.traslation{handles.TP}(3))+1; center(3)= handles.z_SP{handles.TP};
handles.x_SP{handles.TP} = round(mean(x)) + handles.traslation{handles.TP}(1); center(1)= handles.x_SP{handles.TP};
if isfield(handles,'y_SP')
    if length(handles.y_SP)>=handles.TP
        if isempty(handles.y_SP{handles.TP})
            handles.y_SP{handles.TP} = 0; 
            handles.min_y{handles.TP} = 0; 
        end
    else
        handles.y_SP{handles.TP} = 0; 
        handles.min_y{handles.TP} = 0;             
    end
else
    handles.y_SP{handles.TP} = 0; 
    handles.min_y{handles.TP} = 0;             
end

center(2)= handles.y_SP{handles.TP};
%         center


[handles.min_x{handles.TP}, handles.min_y{handles.TP}, handles.min_z{handles.TP}]=displayProjections(V,center,handles);
guidata(handles.figure_selectTP3D,handles); 
% UIWAIT makes f05_selectTerminalPoint3D wait for user response (see UIRESUME)
% uiwait(handles.figure_selectTP3D);


% --- Outputs from this function are returned to the command line.
function varargout = f05_selectTerminalPoint3D_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

% --- Executes on button press in Nextbutton.
function Nextbutton_Callback(hObject, eventdata, handles)
% hObject    handle to Nextbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if isfield(handles,'x_SP')
    if handles.TP == handles.TP_initial
        set(handles.Previousbutton,'Enable','on') 
    end

    handles.TP = handles.TP +1;
    if handles.TP == handles.TP_final
        set(handles.Nextbutton,'Enable','off') 
    end
    set(gcf,'name',['GUI - TP ' num2str(handles.TP) ])
    handles.current_name = get_stackName(handles.stack_name_prefix,handles.TP);

    V = readStack(handles.folder_path,handles.current_name);


    if not(isempty(handles.traslation{handles.TP}))
        center = [handles.x_SP{handles.TP} handles.y_SP{handles.TP} handles.z_SP{handles.TP}];
    else
        center = [];
        handles.x_SP{handles.TP} = handles.x_SP{handles.TP-1} +0;
        handles.y_SP{handles.TP} = handles.y_SP{handles.TP-1} +0 ;
        handles.z_SP{handles.TP} = 0 ;
        handles.traslation{handles.TP} = handles.traslation{handles.TP-1};
        center = [handles.x_SP{handles.TP} handles.y_SP{handles.TP} handles.z_SP{handles.TP}];
    end
    [handles.min_x{handles.TP}, handles.min_y{handles.TP}, handles.min_z{handles.TP}]=displayProjections(V,center,handles);

    guidata(hObject,handles);
end

% --- Executes on button press in Previousbutton.
function Previousbutton_Callback(hObject, eventdata, handles)
% hObject    handle to Previousbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if handles.TP == handles.TP_final
    set(handles.Nextbutton,'Enable','on') 
end

handles.TP = handles.TP -1;
if handles.TP == handles.TP_initial
    set(handles.Previousbutton,'Enable','off') 
end

set(gcf,'name',['GUI - TP ' num2str(handles.TP) ])
handles.current_name = get_stackName(handles.stack_name_prefix,handles.TP);

V = readStack(handles.folder_path,handles.current_name);


if not(isempty(handles.traslation{handles.TP}))
    center = [handles.x_SP{handles.TP} handles.y_SP{handles.TP} handles.z_SP{handles.TP}];
else
    center = [];
end
[handles.min_x{handles.TP}, handles.min_y{handles.TP}, handles.min_z{handles.TP}]=displayProjections(V,center,handles);

guidata(hObject,handles);


% --- Executes on button press in FinishSelectionbutton.
function FinishSelectionbutton_Callback(hObject, eventdata, handles)
% hObject    handle to FinishSelectionbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on key press with focus on figure_selectTP3D and none of its controls.
function figure_selectTP3D_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to figure_selectTP3D (see GCBO)
% eventdata  structure with the following fields (see FIGURE)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
switch eventdata.Key
    
    case 'n'
        if handles.TP < handles.TP_final & isfield(handles,'x_SP')
            Nextbutton_Callback(hObject, eventdata, handles);
        end
    case 'p'
        if handles.TP > handles.TP_initial
            Previousbutton_Callback(hObject, eventdata, handles);
        end        
        
end



function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on mouse press over axes background.
function axes1_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to axes2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if strcmp( get(handles.figure_selectTP3D,'selectionType') , 'normal')
disp('Left Click')
end
if strcmp( get(handles.figure_selectTP3D,'selectionType') , 'open')
disp('Left Double Click')
end


% --- Executes on mouse press over axes background.
function axes2_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to axes2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on mouse press over axes background.
function axes3_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to axes3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

function ima_ = get_image_to_show(V)
%     V=-V;

    %para homogeneizar las intensidades
%     V = V - imclose(imopen(V,ones(10,10,1)),ones(10,10,1));
% 
% 
%     max_value_CF = 20;
% 
%     I = V >max_value_CF;
%     V(I) =max_value_CF;

% I = V==0;
% min_val = min(V(~I));
% V(V<min_val) = min_val;
V = V - imclose(imopen(V,ones(10,10,1)),ones(10,10,1));

max_value_CF = 50;
I = V >max_value_CF;
V(I) =max_value_CF;

    ima_ = max(V,[],3)';

function ima_ = get_image_to_show1(V)
%     V=-V;
    if size(V,1)<300
        V = V - imclose(imopen(V,ones(10,10,1)),ones(10,10,1));
        V(V>20)=20;
    end
    
    I = V<5; I= imdilate(I,ones(1,1,3));V = V.*uint8(not(I));
    
    for i=1:size(V,3)
        for t=1:3
            V(:,:,i) = (medfilt2(V(:,:,i),[3 3]));
        end
%         nx_c = round(size(V,1)/2);
%         ny_c = round(size(V,2)/2);
%         profile(i)=sum(sum(single(V(nx_c-5:nx_c+5,ny_c-5:ny_c+5,i))));
    end
    
%     n_d = 5;
%     
%     nx = floor(size(V,1)/n_d);
%     ny = floor(size(V,2)/n_d);
%     proj = 0*V;
%     for i=1:nx-1
%         for j=1:ny-1
%             min_x = n_d*(i-1)+1;
%             min_y = n_d*(j-1)+1;
%             max_val = -inf;
%             for z=2:3:size(V,3)-1
%                 c_V = V(min_x:min_x+n_d,min_y:min_y+n_d,z-1:z+1);
%                 mean_val = mean(c_V(:));
%                 if mean_val>max_val
%                     max_val = mean_val;
%                     proj(min_x:min_x+n_d,min_y:min_y+n_d,:)=0;
%                     proj(min_x:min_x+n_d,min_y:min_y+n_d,z-1:z+1) = V(min_x:min_x+n_d,min_y:min_y+n_d,z-1:z+1);
%                 end
%             end
%         end
%     end
%     V = proj;
    
%     [~,ind]=max(smooth(profile,3));
    
%     V = imclose(V,ones(3,3,1));
%     V = convn(V,ones(3,3,5)/27,'same');
    
%     ima_ = imfilter(max(V,[],3)',ones(5,5)/25);
    if (size(V,1)<256)
%         nx_c = round(size(V,1)/2);
%         ny_c = round(size(V,2)/2);        
%         [~,ind] = max(V(nx_c-5:nx_c+5,ny_c-5:ny_c+5,:),[],3);
%         ind = round(mean(ind(:)));
% %         V(I)=0;
%         ima_ = max(V(:,:,ind-5:ind+5),[],3)';
        
         ima_ = max(V,[],3)';
%          ima_ = sum(V,3)';

%         [~,ima_] = max(V,[],3);
%         ima_ =ima_';
        
%         ima_ = max(V,[],3)';
    else
        ima_ = max(V,[],3)';
    end
