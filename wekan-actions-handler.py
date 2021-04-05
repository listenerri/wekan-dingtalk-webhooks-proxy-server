#!/usr/bin/env python3
# coding = utf-8
# author = listenerri
# maintainer = listenerri

__Common_Header = ""
__Common_Tail = ""

__Action_2_Delivery_Temp = {
    "act-addAttachment": "{user} 添加了附件\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-deleteAttachment": "{user} 移除了附件\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-addSubtask": "{user} 添加了子任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-addedLabel": "{user} 添加了标签\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-removedLabel": "{user} 移除了标签\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-addChecklist": "{user} 添加了清单\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-addChecklistItem": "{user} 添加了清单项\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-removeChecklist": "{user} 移除了清单\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-removeChecklistItem": "{user} 移除了清单项\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-checkedItem": "{user} 完成了清单项\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-uncheckedItem": "{user} 恢复了清单项\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-completeChecklist": "{user} 完成了清单\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-uncompleteChecklist": "{user} 恢复了清单\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-addComment": "{user} 评论了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-editComment": "{user} 编辑了任务评论\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-deleteComment": "{user} 删除任务评论\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-createBoard": "{user} 创建了看板\n看板：{board}",
    "act-createSwimlane": "{user} 创建了泳道\n看板：{board}",
    "act-createCard": "{user} 创建了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-createCustomField": "{user} 创建了自定义字段\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-deleteCustomField": "{user} 删除了自定义字段\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-setCustomField": "{user} 修改了自定义字段\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-createList": "{user} 创建了列表\n看板：{board}\n列表：{list}",
    "act-addBoardMember": "{user} 添加了看板成员\n看板：{board}",
    "act-archivedBoard": "{user} 归档了看板\n看板：{board}",
    "act-archivedCard": "{user} 归档了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-archivedList": "{user} 归档了列表\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-archivedSwimlane": "{user} 归档了泳道\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-joinMember": "{user} 增加了任务成员\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-moveCard": "{user} 移动了卡片\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-moveCardToOtherBoard": "{user} 移动了卡片\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-removeBoardMember": "{user} 移除了看板成员\n看板：{board}",
    "act-restoredCard": "{user} 恢复了任务\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-unjoinMember": "{user} 移除了任务成员\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-a-dueAt": "{user} 修改了任务到期时间\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-a-endAt": "{user} 修改了任务结束时间\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-a-startAt": "{user} 修改了任务开始时间\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-a-receivedAt": "{user} 修改了任务接收时间\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-newDue": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-withDue": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-almostdue": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-pastdue": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}",
    "act-duenow": "{user} 任务到期提醒\n看板：{board}\n列表：{list}\n任务：{card}"
}

__Action_2_Handler = {

}

def get_delivery(wekan_action):
    pass
