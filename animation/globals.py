
class AnimConstants():
    
    animcontrol_attr     = 'animControl'
    mirror_attr          = 'mirrorAxis'
    world_attr           = 'worldType'    
    target_attr          = 'targetNode'
    pos_attr             = 'posNode'
    riglabel_attr        = 'rigLabel'
    ignore_attr          = 'ignore'
    rigdata_attr         = 'rigData'
    rignode_attr         = 'rigNode'
    is_tagged_attr       = 'tagged'
    component_data_attr  = 'controlShapeData'
    

    
    # common attribute parameters
    translate     = ['translateX', 'translateY', 'translateZ']
    rotate        = ['rotateX', 'rotateY', 'rotateZ']
    scale         = ['scaleX', 'scaleY', 'scaleZ']
    vis           = ['visibility']
    radius        = ['radius']
    rotationOrder = ['rotateOrder']
    jointOrient   = ['jointOrientX', 'jointOrientY', 'jointOrientZ']
    
    # all attributes
    all_channels = translate + rotate + scale + vis

    FK     = 'FK'
    IK     = 'IK'
    TOGGLE = 'TOGGLE'

    # ikck chain attributes
    chain_switch            = 'switcher'
    chain_experssion_attr   = ['swicthExp1Index', 'switchExp2Index']
    chain_control           = 'switchControls'
    chain_ik_controls       = 'swicthIkControls'
    chain_fk_controls       = 'switchFkControls'    
    
    # animation tools
    ikfk_limb_main       = 'ikFkLimb_main'
    ikfk_limb_ikcontrol  = 'ikFkLimb_ikControl'
    ikfk_limb_ikpvcontrol  = 'ikFkLimb_ikPv'
    ikfk_limb_iktrig       = 'ikFkLimb_ikPVTriangle'
    ikfk_limb_ik_rot_match  = 'ikFkLimb_ikRotMatch'
    ikfk_limb_fk_control   = 'ikFkLimb_fk'
    ikfk_limb_skin_joint  = 'ikFkLimb_skin'
    ikfk_limb_foot_roll   = 'ikFkLimb_footRoll'
    ikfk_limb_toe_joint   = 'ikFkLimb_toeJoint'
    ikfk_limb_toe_fk      = 'ikFkLimb_toeFk'
    ikfk_limb_ikpv_distance   =  10.0
    
    gimbal_vis                 = 'GimbalVis'
    off_on_attr                = {'onOff':'Off:On'}    
    ikfk_switch_shape          = 'ikfk_switch'
    ikfk_tag_attr              = 'ikfk_tag'
    ikfk_blend_attr            = {'ikBlend':'fk:ik:'}
    ik_stretch_onoff_attr      = {'stretch':'off:on:'}
    ik_stretch_extend_attr     = ['extendHi', 'extendLo']
    ik_stretch_additive_attr   = 'additive'
    ik_stretch_node_onoff_attr = 'onOff'
    ik_noodle_affix            = 'Nl'
    ik_noodle_inter            = 'Im'
    ik_noodle_loc              = 'ndleLoc'
    ik_noodle_name             = 'Noodle'
    limb_nodes                 = 'limbNodes'
    parentspace                = 'parent'
    stretch_extend_lo          = 'extendLo' 
    stretch_extend_hi          = 'extendHi'    
    
#class Globals(object):
    
anim = AnimConstants()

    #def __init__(self):
        #pass