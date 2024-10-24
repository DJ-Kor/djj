import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import { useQuery, useMutation } from "@apollo/client";
import {
  getLEDPriceManagementBase,
  addLEDPriceManagementBase,
  updateLEDPriceManagementBase,
  deleteLEDPriceManagementBase,
} from "../gql/gql_price";
import {
  LEDOS_SAVE_LOG_ES,
  LEDOS_DOWNLOAD_LOG_ES,
  LEDOS_UPLOAD_LOG_ES,
  LEDOS_HISTORY_LOG_ES,
} from "../gql/gql_ledoscommon";
import _ from "lodash";
import ExcelJS from "exceljs";
// component
import PricingTable from "./component/PricingTable";
import HistoryDialog from "./component/HistoryDialog";
import { Spinner } from "~/components/Spinner";
import {
  DialogTitle,
  DialogContent,
  DialogContentText,
} from "~/components/Dialog";
import ContentBody from "~/components/ContentBody";
// mui
import {
  Grid,
  Container,
  Button,
  Dialog,
  DialogActions,
  Box,
  ListItemText,
  Menu,
  MenuItem,
  Typography,
  TextField,
  Tooltip,
} from "@mui/material";
import { makeStyles } from "@mui/styles";
import { withStyles } from "@mui/styles";
// mui - icon
import HistoryIcon from "@mui/icons-material/History";
import RedoIcon from "@mui/icons-material/Redo";
import UndoIcon from "@mui/icons-material/Undo";
import GetAppIcon from "@mui/icons-material/GetApp";
import PublishIcon from "@mui/icons-material/Publish";
import SaveIcon from "@mui/icons-material/Save";
import ClearIcon from "@mui/icons-material/Clear";
import TrackChangesIcon from "@mui/icons-material/TrackChanges";
import client_config from "~/config/client_config.json";
const env = process.env.REACT_APP_RELEASE || "development";
const config = client_config[env];
import { HotTable } from "@handsontable/react";
import "handsontable/dist/handsontable.full.min.css";

export const TestHandsOnTable = (props) => {
  const [data, setData] = useState([]);

  // if (l1) {
  //   return (
  //     <Box height="90vh" display="flex">
  //       <Spinner />
  //     </Box>
  //   );
  // }
  // if (e1) {
  //   return <div>Error</div>;
  // }
  // if (!d1) return null;

  const handleReset = () => {
    setHandsonData(_.cloneDeep(clonedData));
    hotTable.current.hotInstance.render();
  };

  const clearFilters = () => {
    hotTable.current.hotInstance.getPlugin("Filters").clearConditions();
    hotTable.current.hotInstance.getPlugin("Filters").filter();
    hotTable.current.hotInstance.render();
  };

  const undoHandler = () => {
    if (hotTable.current) {
      hotTable.current.hotInstance.undo();
    }
  };

  const redoHandler = () => {
    if (hotTable.current) {
      hotTable.current.hotInstance.redo();
    }
  };

  const handleDownloadMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleDownloadMenuClose = () => {
    setAnchorEl(null);
  };

  const handleHistoryDialogOpen = () => {
    historyLogESHandler();
    setHistoryDialogOpen(true);
  };

  return (
    <ContentBody>
      <Container>
        <Grid container spacing={1}>
          이거이거이거이거이거
          <Grid container spacing={3}>
            <HotTable
              data={[
                ["", "Tesla", "Volvo", "Toyota", "Ford"],
                ["2019", 10, 11, 12, 13],
                ["2020", 20, 11, 14, 13],
                ["2021", 30, 15, 12, 13],
              ]}
              rowHeaders={true}
              colHeaders={true}
              height="auto"
              autoWrapRow={true}
              autoWrapCol={true}
              licenseKey="non-commercial-and-evaluation" // for non-commercial use only
            />
          </Grid>
        </Grid>
      </Container>
    </ContentBody>
  );
};

export default React.memo(TestHandsOnTable);
