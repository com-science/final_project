START_MONEY = 10000  # 초기 자본
PLAYER_NO = 2  # 플레이어의 수
ROW_OF_REGIONS = 10 # 한 행에 있는 땅의 개수
COLUMN_OF_REGIONS = 10 # 한 열에 있는 땅의 개수
TOTAL_REGIONS = ((ROW_OF_REGIONS - 1) + (COLUMN_OF_REGIONS - 1)) * 2  # 총 땅의 수
MAXIMUM_TURN = 20  # 진행할 최대 턴 수
STOP_TURN = 1  # 무인도에 갔을 때 멈추어 있을 턴의 수
SALARY = 2000  # 플레이어가 한 바퀴를 돌았을 떄 추가할 돈의 양
TOLL_RATE = 0.01  # 통행료 비율 (땅의 가격 대비 비율)
UPGRADE_RATE = 1.25  # 업그레이드 비용의 비율 (땅의 가격 대비 비율)
CHANGE_OWNER_RATE = 1.4  # 소유자를 바꿀 떄 드는 비용의 비율 (땅의 가격 대비 비율)

REGION_FIRST_BUY = 1  # 땅을 처음 산 경우
REGION_CHANGE_OWNER = 2  # 땅의 소유자가 바뀌는 경우
REGION_UPGRADE = 3  # 땅을 업그레이드 하는 경우

ASK_BUY_MESSAGE = {
    REGION_FIRST_BUY: "Do you want buy this region?($%d)",
    REGION_CHANGE_OWNER: "Do you want to buy this region?($%d)",
    REGION_UPGRADE: "Do you want to upgrade this region?($%d)",
}