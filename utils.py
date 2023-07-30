import ipywidgets as widgets


def show_anns(anns, axes=None):
    if len(anns) == 0:
        return
    if axes:
        ax = axes
    else:
        ax = plt.gca()
        ax.set_autoscale_on(False)
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    polygons = []
    color = []
    for ann in sorted_anns:
        m = ann['segmentation']
        img = np.ones((m.shape[0], m.shape[1], 3))
        color_mask = np.random.random((1, 3)).tolist()[0]
        for i in range(3):
            img[:,:,i] = color_mask[i]
        ax.imshow(np.dstack((img, m*0.5)))
#---------------------------------------------------       
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='red', marker='o', s=80, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='o', s=80, edgecolor='white', linewidth=1.25)  
#---------------------------------------------------
def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=1)
    else:
        color = np.array([200/255, 0/255, 0/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
#---------------------------------------------------   
def custom_plot(title,image,specific_point):
    input_label = np.array([1])
    #--------------
    masks = mask_generator_2.generate(image)
    
    print('masks')
    #--------------
    predictor.set_image(image)
    masks_p, scores, logits = predictor.predict(
        point_coords=specific_point,
        point_labels=input_label,
        multimask_output=True,
    )
    return masks, masks_p, scores, logits
    #--------------
#     fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))
#     #fig.suptitle(f'{title} tumor')
#     plt.axis('off')
#     ax1.imshow(image)
#     ax1.title.set_text("Image")
#     ax2.imshow(image)
#     ax2.title.set_text("Image+Masks")
#     show_anns(masks, ax2)
#     for i, (mask, score) in enumerate(zip(masks_p, scores)):
#         if i==0:
#             ax3.imshow(image)
#             ax3.title.set_text("a specific object")
#             show_points(specific_point, input_label, ax3)
#             show_mask(mask, ax4)
#             ax4.title.set_text(f"Mask - Score: {score:.3f}")
#     for ax in fig.get_axes():
#         ax.label_outer()
#         ax.axis('off')
#-----------------
def draw(img_id):    
    polygon = polygon_map[img_id]
    img = cv2.imread(img_map[img_id])

    blood_vessel = 0
    glomerulus = 0
    unsure = 0
    annotations = []
    for anno in polygon['annotations']:
        if anno['type'] == 'blood_vessel':
            color = (0,255,0)
            blood_vessel += 1
            
        elif anno['type'] == 'glomerulus':
            color = (0,0,0)
            glomerulus += 1
        else:
            color = (255,0,0)
            unsure += 1

        pts = anno['coordinates']
        pts = np.array(pts)
        pts = pts.reshape(-1, 1, 2)
        annotations.append(pts)
        cv2.polylines(img, pts, True, color, 3)
    
    print(f'{blood_vessel = }')
    print(f'{glomerulus = }')
    print(f'{unsure = }')

    plt.imshow(img)
    return annotations

#----------
def draw_sam(img_id, annotations):
    image = cv2.cvtColor(
        cv2.imread('/kaggle/input/hubmap-hacking-the-human-vasculature/train/' + img_id + '.tif'), 
        cv2.COLOR_BGR2RGB
    )
    specific_point = np.array([[50, 100]])
    #custom_plot(img_id, image, specific_point)
    (aa, a, b, c) = custom_plot(img_id, image, specific_point)
    return (aa, a, b, c)
    
output = widgets.Output()

@output.capture()
def ipydisplay(change):
    img_id = change['new']
    ipd.clear_output()
    print("Drawing....")
    annotations = draw(img_id)
    print("Finished Drawing. SAM starting...")
#     print(annotations)
    draw_sam(img_id, annotations)
    plt.axis('off')
    plt.show()
    

def draw_sam(img_id, annotations):
    image = cv2.cvtColor(
        cv2.imread('../input/player-segmentation/0_500/images/' + str(img_id) + '.jpg'), 
        cv2.COLOR_BGR2RGB
    )
    specific_point = np.array([[50, 100]])
    return custom_plot(img_id, image, specific_point)
    
#(masks, masks_p, scores, logits) = draw_sam(2, None)
#masks_p, scores, logits
# you can only use this widget when actually running the notebook
# select = widgets.Dropdown(options=list(polygon_map.keys()))
# select.observe(ipydisplay, 'value')
# widgets.VBox([select, output])
