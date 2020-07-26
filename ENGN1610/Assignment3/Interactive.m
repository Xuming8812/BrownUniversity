function varargout = Interactive(varargin)
% INTERACTIVE MATLAB code for Interactive.fig
%      INTERACTIVE, by itself, creates a new INTERACTIVE or raises the existing
%      singleton*.
%
%      H = INTERACTIVE returns the handle to a new INTERACTIVE or the handle to
%      the existing singleton*.
%
%      INTERACTIVE('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in INTERACTIVE.M with the given input arguments.
%
%      INTERACTIVE('Property','Value',...) creates a new INTERACTIVE or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Interactive_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Interactive_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Interactive

% Last Modified by GUIDE v2.5 22-Oct-2018 16:40:44

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Interactive_OpeningFcn, ...
                   'gui_OutputFcn',  @Interactive_OutputFcn, ...
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


% --- Executes just before Interactive is made visible.
function Interactive_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Interactive (see VARARGIN)

% Choose default command line output for Interactive
handles.output = hObject;

% Update handles structure


handles.mode = true;


handles.newEnd = false;


handles.x0 = -1;

handles.y0 = -1;

handles.x1 = -1;

handles.y1 = -1;


handles.fileName = '';


handles.OriginImage=[];
handles.MarkedImage=[];
guidata(hObject, handles);

set(handles.axes1,'Visible','off');

set(handles.btnSelectStart,'Enable','off');
set(handles.btnSelectNext,'Enable','off');
set(handles.btnClearLines,'Enable','off');

% UIWAIT makes Interactive wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Interactive_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in btnLoadImage.
function btnLoadImage_Callback(hObject, eventdata, handles)
% hObject    handle to btnLoadImage (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[filename,pathnam] = uigetfile('.pgm','Please select the image file');

%if the filename is not null
if filename~= 0
    
    %save the filename
    handles.fileName = filename;
    guidata(hObject, handles);
    
    %show the image in axes1
    axis(handles.axes1);
    imshow(filename);
    
    %save the original image in matrix
    handles.OriginImage = imread(filename);
    guidata(hObject, handles);
    
    %initialize the MarkedImage
    handles.MarkedImage = handles.OriginImage;
    guidata(hObject, handles);
    
    %refresh the coordinate of starting and ending points
    handles.x0 = -1;
    guidata(hObject, handles);
    
    handles.y0 = -1;
    guidata(hObject, handles);
    
    handles.x1 = -1;
    guidata(hObject, handles);
   
    handles.y1 = -1;
    guidata(hObject, handles);

    %enable button select start pixel
    set(handles.btnSelectStart,'Enable','on');
    
end


% --- Executes on button press in radioBoundary.
function radioBoundary_Callback(hObject, eventdata, handles)
% hObject    handle to radioBoundary (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.mode = true;
guidata(hObject, handles);

% Hint: get(hObject,'Value') returns toggle state of radioBoundary


% --- Executes on button press in radioCenterline.
function radioCenterline_Callback(hObject, eventdata, handles)
% hObject    handle to radioCenterline (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.mode = false;
guidata(hObject, handles);

% Hint: get(hObject,'Value') returns toggle state of radioCenterline


% --- Executes on button press in btnSelectStart.
function btnSelectStart_Callback(hObject, eventdata, handles)
% hObject    handle to btnSelectStart (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

[x,y] = ginput(1);

[rowNum_I,colNum_I] = size(handles.OriginImage);

% make sure the input coordinate is within the range of the image
if x>0 && x<=colNum_I && y>0 && y<=rowNum_I
    
    %update the stored value
    handles.x0 = round(x);
    guidata(hObject, handles);
    handles.y0 = round(y);
    guidata(hObject, handles);
    
    
    handles.x1 = -1;
    guidata(hObject, handles);
    handles.y1 = -1;
    guidata(hObject, handles);
    
    %show the coordinate in the control
    set(handles.txtPosX,'string',num2str(round(x)));
    set(handles.txtPosY,'string',num2str(round(y)));

    set(handles.btnSelectNext,'Enable','on');    
end




% --- Executes on button press in btnSelectNext.
function btnSelectNext_Callback(hObject, eventdata, handles)
% hObject    handle to btnSelectNext (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
[x,y] = ginput(1);

[rowNum_I,colNum_I] = size(handles.OriginImage);

% make sure the input coordinate is within the range of the image
if x>0 && x<=colNum_I && y>0 && y<=rowNum_I
    if handles.x1 == -1 && handles.y1 == -1
    
    else
         %update the stored starting value
        handles.x0 = handles.x1;
        guidata(hObject, handles);
        handles.y0 = handles.y1;   
        guidata(hObject, handles);
    end
        %update the stored value
        handles.x1 = round(x);
        guidata(hObject, handles);
        handles.y1 = round(y);
        guidata(hObject, handles);
        %show the coordinate in the control
        set(handles.txtPosX,'string',num2str(round(x)));
        set(handles.txtPosY,'string',num2str(round(y)));
    
    %calculate the shortest path for starting pixel and ending pixel
    if handles.mode == true
        p = BoundaryDetection(handles.OriginImage,handles.x0,handles.y0,handles.x1,handles.y1);
    else
        p = CenterlineDetection(handles.OriginImage,handles.x0,handles.y0,handles.x1,handles.y1);   
    end
    %draw the path on the image
    handles.MarkedImage = DrawLines(handles.MarkedImage,p);
    guidata(hObject, handles);

    %show the image as well as the original image
    axis(handles.axes1);
    imshow(handles.MarkedImage);
    set(handles.btnClearLines,'Enable','on');
end



% --- Executes on button press in btnClearLines.
function btnClearLines_Callback(hObject, eventdata, handles)
% hObject    handle to btnClearLines (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.MarkedImage = handles.OriginImage;
guidata(hObject, handles);
axis(handles.axes1);
imshow(handles.MarkedImage);



function txtPosX_Callback(hObject, eventdata, handles)
% hObject    handle to txtPosX (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of txtPosX as text
%        str2double(get(hObject,'String')) returns contents of txtPosX as a double


% --- Executes during object creation, after setting all properties.
function txtPosX_CreateFcn(hObject, eventdata, handles)
% hObject    handle to txtPosX (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function txtPosY_Callback(hObject, eventdata, handles)
% hObject    handle to txtPosY (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of txtPosY as text
%        str2double(get(hObject,'String')) returns contents of txtPosY as a double


% --- Executes during object creation, after setting all properties.
function txtPosY_CreateFcn(hObject, eventdata, handles)
% hObject    handle to txtPosY (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
