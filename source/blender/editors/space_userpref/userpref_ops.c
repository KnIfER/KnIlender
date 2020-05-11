/*
 * ***** BEGIN GPL LICENSE BLOCK *****
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version. 
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * The Original Code is Copyright (C) 2008 Blender Foundation.
 * All rights reserved.
 *
 * 
 * Contributor(s): Blender Foundation
 *
 * ***** END GPL LICENSE BLOCK *****
 */

/** \file blender/editors/space_userpref/userpref_ops.c
 *  \ingroup spuserpref
 */


#include <string.h>
#include <stdio.h>

#include "ED_screen.h"
#include "ED_space_api.h"

#include "BKE_context.h"

#include "WM_api.h"
#include "WM_types.h"

#include "userpref_intern.h"


static int userpref_view_info_poll(bContext *C)
{
	return true;
}

static int userpref_view_info_exec(bContext *C, wmOperator *op)
{
	ScrArea *sa = CTX_wm_area(C);
	ARegion *ar = CTX_wm_region(C);
	bScreen *screen = CTX_wm_screen(C);
	// dedined with wm.context_set_enum
}

void USERPREF_OT_view_info(wmOperatorType *ot)
{
	/* identifiers */
	ot->name = "View Info";
	ot->idname = "USERPREF_OT_view_info";
	ot->description = "View Info Panel";

	/* api callbacks */
	ot->poll = userpref_view_info_poll;
	ot->exec = userpref_view_info_exec;

	/* flags */
	ot->flag = OPTYPE_REGISTER | OPTYPE_UNDO;
}