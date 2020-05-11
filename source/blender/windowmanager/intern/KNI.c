#include "KNI.h"

#include "ED_anim_api.h"
#include "ED_screen.h"

static bool equal_verts(ScrVert* a, ScrVert* b){
	return a->vec.x==b->vec.x && a->vec.y==b->vec.y;
}

static bool isDirectRightNeighbourTo(ScrArea* now, ScrArea* sa){
	return equal_verts(now->v2, sa->v3) && equal_verts(now->v1, sa->v4);
}

//static void printVertXY(ScrArea *area){
//	printf("vert:\n %d, %d   %d, %d \n %d, %d   %d, %d \n"
//		, area->v1->vec.x, area->v1->vec.y
//		, area->v2->vec.x, area->v2->vec.y
//		, area->v3->vec.x, area->v3->vec.y
//		, area->v4->vec.x, area->v4->vec.y
//	);
//}

int expand_region_to_right_exec(bContext *C)
{
	ScrArea *sa = CTX_wm_area(C);
	ARegion *ar = CTX_wm_region(C);
	bScreen *screen = CTX_wm_screen(C);

	ScrArea *now = sa;
	while(now){
		now = now->next;
		if(now && isDirectRightNeighbourTo(now, sa)){
			//printf("\n\nfound1 %d  !!!\n", now->spacetype); printVertXY(now);
			break;
		}
	}
	if(!now){
		now = sa;
		while(now){
			now = now->prev;
			if(now && isDirectRightNeighbourTo(now, sa)){
				//printf("\n\nfound2 %d  !!!\n", now->spacetype); printVertXY(now);
				break;
			}
		}
	}
	if(now){
		//printf("邻居宽度：%d \n", now->winx);
		short newRight = 0;
		if(now->winx<35){
			newRight = now->winx + sa->winx;
			newRight = newRight/2 + 35;
		} else {
			newRight=now->v3->vec.x-32;
		}
		sa->v3->vec.x=newRight;
		sa->v4->vec.x=newRight;
	}

	screen->do_refresh=1;
}
