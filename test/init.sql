/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50722
Source Host           : 10.40.5.1:3306
Source Database       : cms1010

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2020-02-27 09:57:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for sys_dict
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict`;
CREATE TABLE `sys_dict` (
                            `id` int(11) NOT NULL AUTO_INCREMENT,
                            `type_code` varchar(20) DEFAULT NULL COMMENT '类型',
                            `value` varchar(20) DEFAULT NULL COMMENT '字典名',
                            `label` varchar(20) DEFAULT NULL COMMENT '字典值',
                            `description` varchar(25) DEFAULT NULL,
                            `create_date` datetime DEFAULT NULL,
                            `create_by` int(11) DEFAULT NULL,
                            `update_date` datetime DEFAULT NULL,
                            `update_by` int(11) DEFAULT NULL,
                            `del_flag` char(1) DEFAULT '0',
                            PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sys_dict
-- ----------------------------
INSERT INTO `sys_dict` VALUES ('1', 'gender', '1', '男', '性别', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('2', 'gender', '2', '女', '性别', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('3', 'orderStatus', '1', '未付款', '订单状态', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('4', 'orderStatus', '2', '待付款', '订单状态', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('5', 'orderStatus', '3', '已付款', '订单状态', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('6', 'orderStatus', '4', '已收货', '订单状态', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('7', 'filmtype', '1', '动作', '类型', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('8', 'filmtype', '2', '剧情', '类型', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('9', 'filmtype', '3', '情感', '类型', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('10', 'filmtype', '4', '记录', '类型', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('11', 'language', '1', '汉语普通话', '语言', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('12', 'language', '2', '汉语粤语', '语言', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('13', 'language', '3', '英语', '语言', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('14', 'language', '4', '法语', '语言', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('15', 'userStatus', '1', '正常', '用户状态', null, null, null, null, '0');
INSERT INTO `sys_dict` VALUES ('16', 'userStatus', '2', '冻结', '用户状态', null, null, null, null, '0');

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu` (
                            `id` bigint(20) NOT NULL AUTO_INCREMENT,
                            `pid` bigint(20) DEFAULT NULL COMMENT '父菜单ID，一级菜单为0',
                            `name` varchar(50) DEFAULT NULL COMMENT '菜单名称',
                            `url` varchar(200) DEFAULT NULL COMMENT '菜单URL',
                            `perms` varchar(500) DEFAULT NULL COMMENT '授权(多个用逗号分隔，如：user:list,user:create)',
                            `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
                            `create_by` int(11) DEFAULT NULL,
                            `create_date` datetime DEFAULT NULL,
                            `update_by` int(11) DEFAULT NULL,
                            `update_date` datetime DEFAULT NULL,
                            `del_flag` char(1) DEFAULT '0',
                            PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='菜单管理';

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES ('1', '0', '系统管理', null, null, '&#xe609;', null, null, null, null, '0');
INSERT INTO `sys_menu` VALUES ('2', '1', '控制台', '/a/console', null, null, null, null, null, null, '0');
INSERT INTO `sys_menu` VALUES ('3', '1', '用户管理', '/a/user/list', null, null, null, null, null, null, '0');
INSERT INTO `sys_menu` VALUES ('4', '1', '菜单管理', '/a/menu/list', null, null, null, null, null, null, '0');
INSERT INTO `sys_menu` VALUES ('5', '1', '角色管理', '/a/role/list', null, null, null, null, null, null, '0');
INSERT INTO `sys_menu` VALUES ('6', '0', '影片管理', null, null, '&#xe857;', null, null, null, null, '0');
INSERT INTO `sys_menu` VALUES ('7', '6', '图集', '/a/album/list', null, null, null, null, null, null, '0');
INSERT INTO `sys_menu` VALUES ('14', '6', '影片列表', '/a/film/list', null, null, null, null, null, null, '0');

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role` (
                            `id` int(11) NOT NULL AUTO_INCREMENT,
                            `name` varchar(255) DEFAULT NULL COMMENT '角色名称',
                            `remark` varchar(255) DEFAULT NULL,
                            `create_by` int(11) DEFAULT NULL,
                            `create_date` datetime DEFAULT NULL,
                            `update_by` int(11) DEFAULT NULL,
                            `update_date` datetime DEFAULT NULL,
                            `del_flag` char(1) DEFAULT NULL,
                            PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES ('1', '超级管理员', 'admin', null, null, null, null, '0');
INSERT INTO `sys_role` VALUES ('2', '分店管理员', null, null, null, null, null, '0');

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu` (
                                 `id` bigint(20) NOT NULL AUTO_INCREMENT,
                                 `sys_role_id` bigint(20) DEFAULT NULL COMMENT '角色ID',
                                 `sys_menu_id` bigint(20) DEFAULT NULL COMMENT '菜单ID',
                                 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8 COMMENT='角色与菜单对应关系';

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
INSERT INTO `sys_role_menu` VALUES ('88', '4', '1');
INSERT INTO `sys_role_menu` VALUES ('89', '4', '2');
INSERT INTO `sys_role_menu` VALUES ('96', '1', '2');
INSERT INTO `sys_role_menu` VALUES ('97', '1', '1');
INSERT INTO `sys_role_menu` VALUES ('98', '1', '3');
INSERT INTO `sys_role_menu` VALUES ('99', '1', '1');
INSERT INTO `sys_role_menu` VALUES ('100', '1', '4');
INSERT INTO `sys_role_menu` VALUES ('101', '1', '1');
INSERT INTO `sys_role_menu` VALUES ('102', '1', '5');
INSERT INTO `sys_role_menu` VALUES ('103', '1', '1');
INSERT INTO `sys_role_menu` VALUES ('104', '1', '7');
INSERT INTO `sys_role_menu` VALUES ('105', '1', '6');
INSERT INTO `sys_role_menu` VALUES ('106', '1', '14');
INSERT INTO `sys_role_menu` VALUES ('107', '1', '6');
INSERT INTO `sys_role_menu` VALUES ('108', '2', '7');
INSERT INTO `sys_role_menu` VALUES ('109', '2', '6');
INSERT INTO `sys_role_menu` VALUES ('110', '2', '14');
INSERT INTO `sys_role_menu` VALUES ('111', '2', '6');

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user` (
                            `id` int(11) NOT NULL AUTO_INCREMENT,
                            `username` varchar(50) DEFAULT NULL,
                            `name` varchar(50) DEFAULT NULL,
                            `password` varchar(255) DEFAULT NULL,
                            `email` varchar(100) DEFAULT NULL,
                            `mobile` varchar(25) DEFAULT NULL,
                            `status` tinyint(10) DEFAULT NULL,
                            `create_by` int(11) DEFAULT NULL,
                            `create_date` datetime DEFAULT NULL,
                            `update_by` int(11) DEFAULT NULL,
                            `update_date` datetime DEFAULT NULL,
                            `del_flag` char(1) DEFAULT '0',
                            PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES ('1', 'admin', null, '$2a$10$7YeyQKrlX/lTktWAOKmqD.3t6.iPMuEKBZ2TOnFe4ei9AESHkWG12', '1104975916@qq.com', '15250420158', '1', null, null, null, null, '0');
INSERT INTO `sys_user` VALUES ('2', 'tony', 'tony', '$2a$10$Obxwu29fB.FXvlNB9tXMHOQZzwZh4MkqsMbGktwJzYCNCZYIMD1ra', '1918082411@qq.com', '15250420158', '1', null, null, null, null, '0');
INSERT INTO `sys_user` VALUES ('3', 'edwarder', '蓝莲花', '$2a$10$jk434mfu4vInG7cIDu57ZuRgt.Q92mbZTfFFU1M2KOsb36KkdVPO.', '110495916@qq.com', '15250420158', '1', null, null, null, null, '0');
INSERT INTO `sys_user` VALUES ('4', 'zhangsan', '张三', '$2a$10$77MrQYpbWfIJHUIzTLNmq.pBw.mctOpOGEv08ZPCB8hHfXvg0KImG', '1', '15250420158', '1', null, null, null, null, '0');

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role` (
                                 `id` int(20) NOT NULL AUTO_INCREMENT,
                                 `sys_user_id` int(20) DEFAULT NULL COMMENT '用户ID',
                                 `sys_role_id` int(20) DEFAULT NULL COMMENT '角色ID',
                                 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COMMENT='用户与角色对应关系';

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES ('1', '1', '1');
INSERT INTO `sys_user_role` VALUES ('10', '5', '2');
INSERT INTO `sys_user_role` VALUES ('11', '2', '2');
INSERT INTO `sys_user_role` VALUES ('12', '6', null);
INSERT INTO `sys_user_role` VALUES ('13', '6', '2');
INSERT INTO `sys_user_role` VALUES ('17', '3', '1');
INSERT INTO `sys_user_role` VALUES ('21', '4', '1');
