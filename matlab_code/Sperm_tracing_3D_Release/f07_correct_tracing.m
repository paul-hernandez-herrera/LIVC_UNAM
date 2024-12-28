function varargout = f07_correct_tracing(varargin)
% F07_CORRECT_TRACING MATLAB code for f07_correct_tracing.fig
%      F07_CORRECT_TRACING, by itself, creates a new F07_CORRECT_TRACING or raises the existing
%      singleton*.
%
%      H = F07_CORRECT_TRACING returns the handle to a new F07_CORRECT_TRACING or the handle to
%      the existing singleton*.
%
%      F07_CORRECT_TRACING('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in F07_CORRECT_TRACING.M with the given input arguments.
%
%      F07_CORRECT_TRACING('Property','Value',...) creates a new F07_CORRECT_TRACING or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before f07_correct_tracing_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to f07_correct_tracing_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help
% f07_correct_tracingZXCGF

% Last Modified by GUIDE v2.5 08-Aug-2021 22:50:40

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @f07_correct_tracing_OpeningFcn, ...
                   'gui_OutputFcn',  @f07_correct_tracing_OutputFcn, ...
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


% --- Executes just before f07_correct_tracing is made visible.
function f07_correct_tracing_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to f07_correct_tracing (see VARARGIN)

%function parameters
handles.folder_path = 'E:\SPERM\Fluorescencia_Campo_Claro\20241203 CC 4000fps Fluo8 4000fps 90hz 20 micras\STACKS\Exp8_stacks\stacks_constant_sampling';
handles.stack_name_prefix = 'Exp8_stacks';
handles.file_name_endpoints = 'Exp8_stacks_endPoints_1.mat';
handles.threshold_head = 120;
handles.seed_point_head = [342 240 9];
handles.stacks_index_to_trace = 5;



V = readStack(handles.folder_path,get_stackName(handles.stack_name_prefix,handles.stacks_index_to_trace));
V = increase_contrast(V);
if exist(fullfile(handles.folder_path,[get_stackName(handles.stack_name_prefix,handles.stacks_index_to_trace) '_trace.swc']),'file')
    handles.swc = readSWC(fullfile(handles.folder_path,[get_stackName(handles.stack_name_prefix,handles.stacks_index_to_trace) '_trace.swc']));
else
    handles.swc = zeros(1,7);
end

%to initialize variable
handles.mouse_pos_axes1 = [-1 -1];
handles.mouse_pos_axes2 = [-1 -1];
handles.mouse_pos_axes3 = [-1 -1];
handles.zoom = 1;
global left_corner_crop_stack head_center_pos flagellums_tip;
left_corner_crop_stack = [1 1];
head_center_pos = [-1 -1 -1];
flagellums_tip = [-1 -1 -1];
handles.left_corner_crop_stack = [1 1];
handles.stack_size = [size(V,1) size(V,2)];
handles.stack_size_Z = size(V,3);
handles.V_original = V;
handles.V = V;
handles.mask = [];
handles.drawing_shape = false;
handles.roi = [];

%setting the display trace true
set(handles.checkbox_display_trace,'value',1);
%set(handles.draw_polygon_xy,'BackgroundColor',[0.94 0.94 0.94])
%set(handles.draw_polygon_xz,'BackgroundColor',[0.94 0.94 0.94])

%set(gcf, 'WindowButtonMotionFcn', {@mouseMove, handles});
set ( gcf, 'Color', [135 206 235]/255 )

update_images_GUI(handles);

% Choose default command line output for f07_correct_tracing
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes f07_correct_tracing wait for user response (see UIRESUME)
% uiwait(handles.figure1);


function file_name = get_stackName(file_name,TP)

% ID = get_TPID2(TP);
ID = get_TPID(TP);

file_name = [file_name '_' ID '_DC'];

    
% --- Outputs from this function are returned to the command line.
function varargout = f07_correct_tracing_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes during object creation, after setting all properties.
function figure1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes on key press with focus on figure1 and none of its controls.
function figure1_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  structure with the following fields (see MATLAB.UI.FIGURE)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)
switch eventdata.Character
    %
    case {'+','a'}
        %increase zoom
        if point_inside_rectangle(handles.mouse_pos_axes1, [1 1], handles.stack_size/handles.zoom) & not(handles.drawing_shape)
            handles.zoom = 2*handles.zoom;
            handles.left_corner_crop_stack = update_zoom_coordinates(handles.left_corner_crop_stack + handles.mouse_pos_axes1, handles.stack_size/handles.zoom, handles.stack_size);
            update_images_GUI(handles);
        end
    case {'-','s'}
        %decrease zoom
        if point_inside_rectangle(handles.mouse_pos_axes1, [1 1], handles.stack_size/handles.zoom) & not(handles.drawing_shape)
            if handles.zoom>1
                %minimum zoom must be equal to 2
                handles.zoom = handles.zoom/2;
                handles.left_corner_crop_stack = update_zoom_coordinates(handles.left_corner_crop_stack + handles.mouse_pos_axes1, handles.stack_size/handles.zoom, handles.stack_size);
                update_images_GUI(handles);
            end
        end        
        
end
guidata(hObject, handles);


function left_corner_crop_stack_c = update_zoom_coordinates(mouse_pos, new_vol_size, stack_size)
    global left_corner_crop_stack;
    left_corner_crop_stack_c = round(mouse_pos) - new_vol_size/2;
    if (left_corner_crop_stack_c(1)<1)
        left_corner_crop_stack_c(1)=1;
    end
    if (left_corner_crop_stack_c(2)<1)
        left_corner_crop_stack_c(2)=1;
    end    
    
    if (left_corner_crop_stack_c(1)+new_vol_size(1)-1>stack_size(1))
        left_corner_crop_stack_c(1) = stack_size(1) - new_vol_size(1)+1;
    end
    
    if (left_corner_crop_stack_c(2)+new_vol_size(2)-1>stack_size(2))
        left_corner_crop_stack_c(2) = stack_size(2) - new_vol_size(2)+1;
    end    
    
    left_corner_crop_stack = left_corner_crop_stack_c;
    
function output = point_inside_rectangle(point,corner_1,corner_2)
    output = false;
    if corner_1(1)>corner_2(1) | corner_1(2)>corner_2(2)
        error('Incorrect rectangle definition');
    end
    if point(1)>=corner_1(1) & point(1)<=corner_2(1) & point(2)>=corner_1(2) & point(2)<=corner_2(2)
        output = true;
    end
    
    
    
function display_projections(V,handles)

    %crop_volume
    V = V(handles.left_corner_crop_stack(1):handles.left_corner_crop_stack(1)+handles.stack_size(1)/handles.zoom-1, handles.left_corner_crop_stack(2):handles.left_corner_crop_stack(2)+handles.stack_size(2)/handles.zoom-1,:);
    
    reSampleFactor=3;
    
    %displaying XY projection
    xy_projection = max(V,[],3)';
    
    h=imshow(xy_projection,[],'Parent', handles.axes1);title('XY','Parent', handles.axes1)
%     set(handles.axes1,'hittest','off')
    set(h,'ButtonDownFcn',{@pickedXY,handles});
    
    %displaying XZ projection
    xz_projection = max(V,[],2); xz_projection=reshape(xz_projection,[size(xz_projection,1) size(xz_projection,3)])';
    xz_projection = xz_projection(end:-1:1,:);
    xz_projection = imresize(xz_projection,[reSampleFactor*size(xz_projection,1) size(xz_projection,2)]) ;
    h=imshow(xz_projection,[],'Parent', handles.axes2);title('XZ','Parent', handles.axes2)    
    set(h,'ButtonDownFcn',{@pickedXZ,handles});
    %@(hObject,eventdata)f07_correct_tracing('axes2_ButtonDownFcn',hObject,eventdata,guidata(hObject))
    
    %displaying YZ projection
    yz_projection = max(V,[],1); yz_projection=reshape(yz_projection,[size(yz_projection,2) size(yz_projection,3)])';
%     yz_projection = yz_projection(end:-1:1,:);
    yz_projection = imresize(yz_projection,[reSampleFactor*size(yz_projection,1) size(yz_projection,2)])' ;
    h=imshow(yz_projection,[],'Parent', handles.axes3);title('YZ','Parent', handles.axes3);colormap('gray')
    set(h,'ButtonDownFcn',{@picked_ZY,handles});
    
function disable_buttons(current_button,handles)
    all_buttons = {handles.draw_polygon_xy handles.draw_polygon_yz handles.draw_polygon_xz handles.set_head_center ...
        handles.set_flagellums_tip handles.pushbutton_undo handles.pushbutton_run};
    for i=1:length(all_buttons)
        if (all_buttons{i}~=current_button)
            set(all_buttons{i},'enable', 'off');
        end
    end
    
function enable_buttons(handles)
    all_buttons = {handles.draw_polygon_xy handles.draw_polygon_yz handles.draw_polygon_xz handles.set_head_center ...
        handles.set_flagellums_tip handles.pushbutton_undo handles.pushbutton_run};
    for i=1:length(all_buttons)
        set(all_buttons{i}, 'enable', 'on');
    end    
    
function display_trace(handles)
    reSampleFactor=3;
    swc = handles.swc;
    
    swc(:,3) = swc(:,3)-handles.left_corner_crop_stack(1)+1; 
    swc(:,4) = swc(:,4)-handles.left_corner_crop_stack(2)+1;
    
    hold(handles.axes1,'all')
    plot(handles.axes1,swc(:,3),swc(:,4),'LineWidth',2);
    hold(handles.axes1,'off')
    
    hold(handles.axes2,'all')
    plot(handles.axes2,swc(:,3),reSampleFactor*(handles.stack_size_Z-swc(:,5)),'LineWidth',2);
    hold(handles.axes2,'off')
    
    hold(handles.axes3,'all')
    plot(handles.axes3,reSampleFactor*swc(:,5),swc(:,4),'LineWidth',2);    
    hold(handles.axes3,'off')

function display_point(handles, index)
    global head_center_pos flagellums_tip left_corner_crop_stack;
    if index ==1
        point_display = head_center_pos;
        label = 'r*';
    elseif index ==2
        point_display = flagellums_tip;
        label = 'g*';        
    end
    if all(point_display(1:2)>[0 0])
        %we have already clicked the head position in xy plane
        hold(handles.axes1,'on')
        plot(handles.axes1,point_display(1)-left_corner_crop_stack(1)+1, point_display(2)-left_corner_crop_stack(2)+1,label,'LineWidth',2);
        hold(handles.axes1,'off')
    end
    if all([point_display(1) point_display(3)]>[0 0])
        %we have already clicked the head position in xz plane
        hold(handles.axes2,'on')
        plot(handles.axes2,point_display(1)-left_corner_crop_stack(1)+1, 3*(size(handles.V,3)-point_display(3)),label,'LineWidth',2);
        hold(handles.axes2,'off')
    end    
    if all([point_display(2) point_display(3)]>[0 0])
        %we have already clicked the head position in xz plane
        hold(handles.axes3,'on')
        plot(handles.axes3, 3*point_display(3), point_display(2)-left_corner_crop_stack(2)+1,label,'LineWidth',2);
        hold(handles.axes3,'off')
    end      
    
function V = increase_contrast(V)

    V = V - imclose(imopen(V,ones(10,10,1)),ones(10,10,1));

    max_value_CF = 100;
    I = V >max_value_CF;
    V(I) =max_value_CF;


% --- Executes on button press in draw_polygon_xy.
function draw_polygon_xy_Callback(hObject, eventdata, handles)
% hObject    handle to draw_polygon_xy (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    if (all(get(handles.draw_polygon_xy,'BackgroundColor')==[0.94, 0.94,0.94]))
        %setting the background
        handles.drawing_shape = true;
        set(handles.draw_polygon_xy,'BackgroundColor',[0 1.0 0]);
        disable_buttons(handles.draw_polygon_xy,handles)
        set(handles.draw_polygon_xy,'enable','off')
        
        %saving data
        guidata(hObject, handles);
        
        handles.roi = drawpolygon(handles.axes1);
        set(handles.draw_polygon_xy,'enable', 'on');
        
        if isempty(handles.roi.Position)
            handles.drawing_shape = false;
            set(handles.draw_polygon_xy,'BackgroundColor',[0.94 0.94 0.94]);
            enable_buttons(handles)
        end
            %no region selected;
            
        %handles.drawing_shape = false;
    else
        handles.drawing_shape = false;
        enable_buttons(handles)
        
        if length(handles.mask)>=10
            %maximum number of undos
            handles.mask(1)= [];
        end
        mask = create_mask_from_roi_xy(handles);
        handles.mask{length(handles.mask)+1} = mask;
        
        handles.V = (handles.V).*uint8(mask); 
        set(handles.draw_polygon_xy,'BackgroundColor',[0.94 0.94 0.94]);
        handles.roi = [];
        
        update_images_GUI(handles);
    end
    return_focus_to_axes(handles,hObject);
    
function mask = create_mask_from_roi_xy(handles)
    roi = handles.roi;
    mask = true(size(handles.V));
    if not(isempty(roi))
        roi.Position = roi.Position + handles.left_corner_crop_stack - [1 1];
        bw = createMask(handles.roi,handles.stack_size(2),handles.stack_size(1));
        
        mask = not(mask);
        for z=1:size(mask,3)
            mask(:,:,z) = not(bw)';
        end
    end
    
function mask = create_mask_from_roi_xz(handles)
    roi = handles.roi;
    mask = true(size(handles.V));
    if not(isempty(roi))
        
        roi.Position(:,2) = roi.Position(:,2)/3; 
        roi.Position = roi.Position + [handles.left_corner_crop_stack(1) 1] - [1 1];
        bw = createMask(handles.roi,size(handles.V,3),size(handles.V,1));
        bw = bw(end:-1:1,:);

        mask = not(mask);
        for z=1:size(mask,2)
            mask(:,z,:) = not(bw)';
        end    
    end
    
function mask = create_mask_from_roi_yz(handles)
    roi = handles.roi;
    mask = true(size(handles.V));
    if not(isempty(roi))    
        roi = handles.roi;
        roi.Position(:,1) = roi.Position(:,1)/3; 
        roi.Position = roi.Position + [1 handles.left_corner_crop_stack(2)] - [1 1];
        bw = createMask(handles.roi,size(handles.V,2),size(handles.V,3));
        
        mask = not(mask);
        for z=1:size(mask,1)
            mask(z,:,:) = not(bw);
        end  
    end
    
    

% --- Executes on mouse motion over figure - except title and menu.
function figure1_WindowButtonMotionFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    C = get(handles.axes1, 'CurrentPoint'); 
    handles.mouse_pos_axes1 = C(1,1:2);
%     handles.mouse_pos_axes1
    
    C = get(handles.axes2, 'CurrentPoint'); 
    handles.mouse_pos_axes2 = C(1,1:2);
    
    C = get(handles.axes3, 'CurrentPoint'); 
    handles.mouse_pos_axes3 = C(1,1:2);    
%     C(1,1:2)
    % Update handles structure
    guidata(hObject, handles);


% --- Executes on button press in draw_polygon_xz.
function draw_polygon_xz_Callback(hObject, eventdata, handles)
% hObject    handle to draw_polygon_xz (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    if (all(get(handles.draw_polygon_xz,'BackgroundColor')==[0.94, 0.94,0.94]))
        %setting the background
        handles.drawing_shape = true;
        set(handles.draw_polygon_xz,'BackgroundColor',[0 1.0 0]);
        disable_buttons(handles.draw_polygon_xz,handles)
        set(handles.draw_polygon_xz,'enable', 'off');
        
        %saving data
        guidata(hObject, handles);
        
        handles.roi = drawpolygon(handles.axes2);
        set(handles.draw_polygon_xz,'enable', 'on');
        
        
        if isempty(handles.roi.Position)
            handles.drawing_shape = false;
            set(handles.draw_polygon_xz,'BackgroundColor',[0.94 0.94 0.94]);
            enable_buttons(handles);
        end
        
    else
        handles.drawing_shape = false;
        enable_buttons(handles)
        
        if length(handles.mask)>=10
            %maximum number of undos
            handles.mask(1)= [];
        end
        mask = create_mask_from_roi_xz(handles);
        handles.mask{length(handles.mask)+1} = mask;
        
        handles.V = (handles.V).*uint8(mask); 
        set(handles.draw_polygon_xz,'BackgroundColor',[0.94 0.94 0.94]);
        handles.roi = [];
        
        update_images_GUI(handles)
    end
    return_focus_to_axes(handles,hObject);


% --- Executes on button press in draw_polygon_yz.
function draw_polygon_yz_Callback(hObject, eventdata, handles)
% hObject    handle to draw_polygon_yz (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    if (all(get(handles.draw_polygon_yz,'BackgroundColor')==[0.94, 0.94,0.94]))
        %setting the background
        handles.drawing_shape = true;
        set(handles.draw_polygon_yz,'BackgroundColor',[0 1.0 0]);
        disable_buttons(handles.draw_polygon_yz,handles)
        set(handles.draw_polygon_yz,'enable', 'off');
        
        %saving data
        guidata(hObject, handles);
        
        handles.roi = drawpolygon(handles.axes3);
        set(handles.draw_polygon_yz,'enable', 'on');
        
        if isempty(handles.roi.Position)
            handles.drawing_shape = false;
            set(handles.draw_polygon_yz,'BackgroundColor',[0.94 0.94 0.94]);
            enable_buttons(handles)
        end
    else
        handles.drawing_shape = false;
        enable_buttons(handles)
        
        if length(handles.mask)>=10
            %maximum number of undos
            handles.mask(1)= [];
        end
        mask = create_mask_from_roi_yz(handles);
        handles.mask{length(handles.mask)+1} = mask;
        
        handles.V = (handles.V).*uint8(mask); 
        set(handles.draw_polygon_yz,'BackgroundColor',[0.94 0.94 0.94]);
        handles.roi = [];
        
        update_images_GUI(handles)
    end
    return_focus_to_axes(handles,hObject);


% --- Executes on button press in set_head_center.
function set_head_center_Callback(hObject, eventdata, handles)
% hObject    handle to set_head_center (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    if (all(get(handles.set_head_center,'BackgroundColor')==[0.94, 0.94,0.94]))
        %setting the background
        handles.drawing_shape = true;
        set(handles.set_head_center,'BackgroundColor',[0 1.0 0]);
        disable_buttons(handles.set_head_center,handles)
        
        %saving data
        guidata(hObject, handles);
        

    else
        handles.drawing_shape = false;
        enable_buttons(handles)
        
        set(handles.set_head_center,'BackgroundColor',[0.94 0.94 0.94]);
        
        update_images_GUI(handles)
        
    end
    return_focus_to_axes(handles,hObject);
    

% --- Executes on mouse press over axes background.
function pickedXY(hObject, eventdata, handles)
% hObject    handle to axes1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global left_corner_crop_stack head_center_pos flagellums_tip;

%   getting mouse position relative to stack XY plane    
    cpt = get(handles.axes1,'CurrentPoint');
    mouse_pos = cpt(1,1:2);
    point = mouse_pos + left_corner_crop_stack -[1 1];  
    
    point = round(point);    
    if (all(get(handles.set_head_center,'BackgroundColor')==[0, 1.0,0]))
        %update head_center_position
        head_center_pos = get_mouse_position_3D(head_center_pos, point, 3); 
        
    elseif (all(get(handles.set_flagellums_tip,'BackgroundColor')==[0, 1.0,0]))
        
        flagellums_tip = get_mouse_position_3D(flagellums_tip, point, 3); 
    end
    update_images_GUI(handles);
    
function pickedXZ(hObject, eventdata, handles)
% hObject    handle to axes1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    global left_corner_crop_stack head_center_pos flagellums_tip;
    
%   getting mouse position relative to stack XZ plane
    cpt = get(handles.axes2,'CurrentPoint');
    mouse_pos = cpt(1,1:2);
    mouse_pos(2) = size(handles.V,3) - (mouse_pos(2)/3);

    point = mouse_pos + [left_corner_crop_stack(1) 1] -[1 1];
        
    point = round(point);
    if (all(get(handles.set_head_center,'BackgroundColor')==[0, 1.0,0]))
        %update head_center_position
        head_center_pos = get_mouse_position_3D(head_center_pos, point, 2);      
    elseif (all(get(handles.set_flagellums_tip,'BackgroundColor')==[0, 1.0,0]))
        %update flagellum's tip
        flagellums_tip = get_mouse_position_3D(flagellums_tip, point, 2);               
    end    
    update_images_GUI(handles);

 
    
function picked_ZY(hObject, eventdata, handles)
% hObject    handle to axes1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global left_corner_crop_stack head_center_pos flagellums_tip;
    
%   getting mouse position relative to stack ZY plane
    cpt = get(handles.axes3,'CurrentPoint');
    mouse_pos = cpt(1,1:2);
    mouse_pos(1) = mouse_pos(1)/3;

    point = mouse_pos + [1 left_corner_crop_stack(2) ] -[1 1];
    
    point = round(point);        
    if (all(get(handles.set_head_center,'BackgroundColor')==[0, 1.0,0]))
        %update head_center_position
        head_center_pos = get_mouse_position_3D(head_center_pos, point, 1);   
                 
    elseif (all(get(handles.set_flagellums_tip,'BackgroundColor')==[0, 1.0,0]))
        %update flagellums_tip
        flagellums_tip = get_mouse_position_3D(flagellums_tip, point, 1);      
    end  
    update_images_GUI(handles);
    
function point = get_mouse_position_3D(current_position, point, plane_missing)
    if plane_missing ==1
        point = [ current_position(1) point(2) point(1)];
    elseif plane_missing ==2
        point = [ point(1) current_position(2)  point(2)];
    elseif plane_missing ==3
        point = [ point(1) point(2) current_position(3) ];
    end
        
    if (point(plane_missing)==-1)
        %we have not given value to the x coordinate
        point(plane_missing) = 1;
    end        
        

% --- Executes on button press in set_flagellums_tip.
function set_flagellums_tip_Callback(hObject, eventdata, handles)
% hObject    handle to set_flagellums_tip (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    if (all(get(handles.set_flagellums_tip,'BackgroundColor')==[0.94, 0.94,0.94]))
        %setting the background
        handles.drawing_shape = true;
        set(handles.set_flagellums_tip,'BackgroundColor',[0 1.0 0]);
        disable_buttons(handles.set_flagellums_tip,handles)
        
        %saving data
        guidata(hObject, handles);
        

    else
        handles.drawing_shape = false;
        enable_buttons(handles)
        
        set(handles.set_flagellums_tip,'BackgroundColor',[0.94 0.94 0.94]);
        
        update_images_GUI(handles);   
    end
    return_focus_to_axes(handles,hObject);
    
function update_images_GUI(handles)
        display_projections(handles.V,handles);
        if get(handles.checkbox_display_trace, 'Value')
            display_trace(handles); 
        end
        display_point(handles,1);         
        display_point(handles,2);

function return_focus_to_axes(handles,hObject)
    set(hObject, 'enable', 'off');
    drawnow; 
    set(hObject, 'enable', 'on');
    guidata(hObject, handles);
    
% --- Executes on button press in checkbox_display_trace.
function checkbox_display_trace_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox_display_trace (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
update_images_GUI(handles)
% Hint: get(hObject,'Value') returns toggle state of checkbox_display_trace
%get(handles.checkbox_display_trace, 'Value')
%return focus to the axis
return_focus_to_axes(handles,hObject);


% --- Executes on button press in pushbutton_undo.
function pushbutton_undo_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton_undo (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    if ~isempty(handles.mask)
        %eliminating last region
        handles.mask(length(handles.mask)) = [];
    end
    
    %updating the volume to the previous state
    mask = true(size(handles.V_original));
    for i=1:length(handles.mask)
        mask = mask & handles.mask{i};
    end
    handles.V = handles.V_original.*uint8(mask);
    
    update_images_GUI(handles)
    guidata(hObject, handles);


% --- Executes on button press in pushbutton_run.
function pushbutton_run_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton_run (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    global head_center_pos flagellums_tip;
    set(handles.pushbutton_run,'BackgroundColor',[1 0 0]);
    disable_buttons(handles.pushbutton_run,handles);
    set(handles.pushbutton_run,'enable', 'off');
    pause(0.25);
    [~, seed_point_head]= correct_trace_rec_fragelo_CampoClaro_stopTerminalPoint_NOSEGMEN(handles.folder_path, handles.stack_name_prefix, handles.stacks_index_to_trace, handles.file_name_endpoints, handles.seed_point_head,handles.threshold_head, handles.V, head_center_pos,flagellums_tip, handles.swc);
    
    enable_buttons(handles)
    set(handles.pushbutton_run,'BackgroundColor',[0.94 0.94 0.94]);
    
    handles.swc = readSWC(fullfile(handles.folder_path,[get_stackName(handles.stack_name_prefix,handles.stacks_index_to_trace) '_trace.swc']));
    update_images_GUI(handles);
    guidata(hObject, handles);
