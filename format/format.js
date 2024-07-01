import React, { useEffect, useState, useCallback } from "react";
// import axios from "axios";
import {
  Container,
  makeStyles,
  Grid,
  Box,
  Button,
  BottomNavigation,
  BottomNavigationAction,
  Typography,
  TextField,
} from "@material-ui/core";
import ListIcon from "@material-ui/icons/List";
import AccountBoxIcon from "@material-ui/icons/AccountBox";
import SearchIcon from "@material-ui/icons/Search";
import ClearIcon from "@material-ui/icons/Clear";
import ContentBody from "~/components/ContentBody";
import { useQuery, useMutation } from "@apollo/react-hooks";
import { GET_USER } from "~/query/user";
import { USER_HISTORY_TRACKER, ADD_USER_HISTORY_TRACKER, LEDOS_GET_PROJECT_INFO } from "../gql/ledos_gql";
import { getLedosPoUpload, DELETE_LEDOS_POs } from "../gql/ledos_gql2";
// import client_config from "~/config/client_config.json";
import Spinner from "~/components/Spinner";
import StandbyProjectStatusTable from "./components/StandbyProjectStatusTable";
import { MuiPickersUtilsProvider, KeyboardDatePicker } from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import _ from "lodash";

// const env = process.env.REACT_APP_RELEASE || "development";
// const config = client_config[env];

const useStyles = makeStyles((theme) => ({
  container: {
    maxWidth: "3840px",
    maxHeight: "2160px",
    padding: "20px",
    alignItems: "center",
  },
  button_groups: {
    width: "100%",
    textAlign: "left",
    marginBottom: "-20px",
  },
  button_color: {
    backgroundColor: "#464646",
    color: "#FFFFFF",
    fontSize: "8pt",
  },
  navStyle: {
    width: "50%",
    borderRadius: "7px",
  },
  bigBox: {
    border: "2px solid black",
    height: "700px",
    width: "100%",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontSize: "36px",
    fontWeight: "bold",
    marginTop: "30px",
  },
}));

const FILTER_OPTIONS = ["Region", "Country", "Project Name", "Corp", "Model", "Transport", "Note", "Sender"];

const FILTER_SEARCH_OPTIONS = [
  "region",
  "country",
  "project_name",
  "corp",
  "model_name",
  "transport",
  "note",
  "created_by",
];

const DEFAULT_FILTER_FORM = {
  region: "",
  country: "",
  project_name: "",
  corp: "",
  model_name: "",
  transport: "",
  note: "",
  created_by: "",
};

export const StandbyProjectStatus = () => {
  const classes = useStyles();
  const title = "LEDOS > 프로젝트 현황 > 대기 프로젝트 Dashboard";
  const [data, setData] = useState([]);
  const [poData, setPOData] = useState([]);
  const [nonMatchingPO, setNonMatchingPO] = useState([]);
  const [userHistoryData, setUserHistoryData] = useState([]);
  const { data: { currentUser: { email = "" } = {} } = {} } = useQuery(GET_USER);
  const { loading: l1, error: e1, data: d1 } = useQuery(LEDOS_GET_PROJECT_INFO);
  const { loading: l2, error: e2, data: d2 } = useQuery(USER_HISTORY_TRACKER);
  // const { loading: l3, error: e3, data: d3 } = useQuery(LEDOS_PO_DATA_COMBINED);
  const { loading: l4, error: e4, data: d4 } = useQuery(getLedosPoUpload);
  const [onlyUpdated, setOnlyUpdated] = useState("all");
  const [filtersSave, setFiltersSave] = useState(DEFAULT_FILTER_FORM);
  const [filteredData, setFilteredData] = useState([]);

  const [startDate, setStartDate] = useState(() => {
    const today = new Date();
    const thisYear = today.getFullYear();
    const start = new Date(`${thisYear}-01-01`);
    return start;
  });
  const [endDate, setEndDate] = useState(() => {
    const today = new Date();
    const thisYear = today.getFullYear();
    const end = new Date(`${thisYear}-12-31`);
    return end;
  });

  const filteredDataHandler = useCallback(
    (filters) => {
      if (!nonMatchingPO || nonMatchingPO.length === 0) return [];
      let tempData = _.cloneDeep(nonMatchingPO);
      tempData = tempData.filter((row) => {
        const itemDate = row.created_at; // unix timestamp
        // const itemDate = new Date(row.created_at);
        return itemDate >= startDate.getTime() && itemDate <= endDate.getTime();
      });
      if (onlyUpdated === "my_project") {
        tempData = tempData.filter((row) => row.created_by?.includes(email));
      }
      FILTER_SEARCH_OPTIONS.forEach((col_name) => {
        if (filters[`${col_name}`] !== null && filters[`${col_name}`] !== "" && filters[`${col_name}`] !== undefined) {
          tempData = tempData.filter((row) => {
            const compare = row[`${col_name}`]?.toLowerCase() || ""; // String
            return compare.includes(filters[`${col_name}`].toLowerCase());
          });
        }
      });
      setFilteredData(tempData);
      setFiltersSave(filters);
    },
    [nonMatchingPO, startDate, endDate, onlyUpdated, email],
  );

  const [addUserHistoryTracker] = useMutation(ADD_USER_HISTORY_TRACKER, {
    update(cache, { data: { esUserHistoryTrackerAdd } }) {
      const data = cache.readQuery({
        query: USER_HISTORY_TRACKER,
      });

      const newData = data.userHistoryTracker.concat(esUserHistoryTrackerAdd);

      cache.writeQuery({
        query: USER_HISTORY_TRACKER,
        data: {
          userHistoryTracker: newData,
        },
      });
    },
  });

  const [deleteLedosPos] = useMutation(DELETE_LEDOS_POs, { refetchQueries: [{ query: getLedosPoUpload }] });

  const mutationHandlers = async (variables, user) => {
    let actionType = "";
    await deleteLedosPos({
      variables: {
        opportunity_code: variables.opportunity_code,
        model_names: variables.model_names,
      },
    }).catch((error) => {
      console.error("Error Deleting!", error);
    });
    actionType = "Delete";

    const messageMaker = () => {
      if (actionType === "Delete") {
        return `프로젝트 <strong>"${variables.model_names.length}"</strong>개(를) 삭제했습니다.<br/>`;
      }
    };

    let user_history_es_parameter = {
      date: new Date(),
      user: user,
      email: email,
      category: "LEDOS",
      page: "대기 프로젝트 현황 Dashboard",
      action: actionType,
      message: messageMaker(),
    };
    await addUserHistoryTracker({
      variables: {
        uhti: user_history_es_parameter,
      },
    });
  };

  useEffect(() => {
    if (d1) {
      setData(d1.ledosProjectData);
      // console.log('-=-=-=-=-=d1.ledosProjectData=-=-=-=-=')
      // console.log(d1.ledosProjectData);
    }
    if (d2) {
      // console.log('-=-=-=-=-=d2.userHistoryTracker-=-=-=-=-=')
      // console.log(d2.userHistoryTracker);
      const filteredHistory = d2.userHistoryTracker
        .filter((item) => item.category === "LEDOS" && item.page === "대기 프로젝트 현황 Dashboard")
        .sort((a, b) => new Date(b.date) - new Date(a.date));
      setUserHistoryData(filteredHistory);
    }
    if (d4) {
      setPOData(d4.getLedosPoUpload);
      // console.log('-=-=-=-=-=d4.getLedosPoUpload=-=-=-=-=')
      // console.log(d4.getLedosPoUpload);
    }
  }, [d1, d2, d4]);

  useEffect(() => {
    if (poData.length > 0 && data.length > 0) {
      const nonMatching = poData.filter(
        (itemB) => !data.some((itemA) => itemA.LGE_OPPORTUNITYNUMBER__C === itemB.opportunity_code),
      );
      setNonMatchingPO(nonMatching);
    }
  }, [poData, data]);

  useEffect(() => {
    if (onlyUpdated) {
      filteredDataHandler(filtersSave);
    }
  }, [filtersSave, filteredDataHandler, onlyUpdated]);

  if (!d1 || !d2 || !d4) return null;
  if (l1 || l2 || l4) {
    return (
      <Box height="90vh" display="flex">
        <Spinner />
      </Box>
    );
  }
  if (e1 || e2 || e4) {
    return <div>Error</div>;
  }

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    return `${year}-${month.toString().padStart(2, "0")}-${day.toString().padStart(2, "0")}`;
  };

  const simpleDateHandler = (type) => {
    const today = new Date();
    let end_date = new Date(today);
    end_date.setDate(today.getDate());
    let start_date = new Date(end_date);
    if (type === 0) {
      start_date.setFullYear(end_date.getFullYear() - 1);
    } else if (type === 1) {
      start_date.setMonth(end_date.getMonth() - 3);
      start_date.setDate(end_date.getDate());
    } else if (type === 3) {
      const thisYear = new Date().getFullYear();
      start_date = new Date(`${thisYear}-01-01`);
      end_date = new Date(`${thisYear}-12-31`);
    } else {
      start_date.setMonth(end_date.getMonth() - 1);
      start_date.setDate(end_date.getDate());
    }
    setStartDate(start_date);
    setEndDate(end_date);
  };

  const DatePicker = () => {
    return (
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
        <KeyboardDatePicker
          style={{ width: "40%" }}
          disableToolbar
          variant="inline"
          format="yyyy-MM-dd"
          margin="normal"
          id="start-date"
          label="Created Date (From)"
          value={formatDate(startDate)}
          onChange={(e) => setStartDate(e)}
          // disableFuture
          maxDate={endDate}
          KeyboardButtonProps={{
            "aria-label": "change date",
          }}
        />
        <KeyboardDatePicker
          style={{ width: "40%", marginBottom: "10px", marginRight: "10px" }}
          disableToolbar
          variant="inline"
          format="yyyy-MM-dd"
          margin="normal"
          id="end-date"
          label="Created Date (To)"
          value={formatDate(endDate)}
          onChange={(e) => setEndDate(e)}
          minDate={startDate}
          KeyboardButtonProps={{
            "aria-label": "change date",
          }}
        />
      </MuiPickersUtilsProvider>
    );
  };

  const onlyUpdatedHandler = (event, newValue) => {
    setOnlyUpdated(newValue);
  };

  const FiltersTextField = () => {
    const [filters, setFilters] = useState(filtersSave);
    const handleKeyDown = (event) => {
      if (event.key === "Enter") {
        filteredDataHandler(filters);
      }
    };

    const resetFilterHandler = () => {
      setFiltersSave({ ...DEFAULT_FILTER_FORM });
      if (onlyUpdated === "my_project") {
        setFilteredData(poData.filter((row) => row.created_by?.includes(email)));
      } else {
        setFilteredData(poData);
      }
    };

    const ResetFilterButton = () => {
      return (
        <Button
          onClick={resetFilterHandler}
          className={classes.button_color}
          variant="contained"
          align="center"
          fullWidth
        >
          <ClearIcon />
          &nbsp;Clear
        </Button>
      );
    };

    const SearchButton = () => {
      return (
        <Button
          onClick={() => filteredDataHandler(filters)}
          className={classes.button_color}
          variant="contained"
          align="center"
          fullWidth
        >
          <SearchIcon />
          &nbsp;Search
        </Button>
      );
    };

    const handleFilterChange = (label, value) => {
      setFilters((prev) => ({
        ...prev,
        [label]: value,
      }));
    };
    return (
      <React.Fragment>
        {FILTER_SEARCH_OPTIONS.map((item, index) => {
          const key = `${item}-${index}`;
          return (
            <Grid item xs={2} key={key}>
              <TextField
                id={`${item}-${index}`}
                key={`${key}-textfield`}
                value={filters[item] || ""}
                onChange={(e) => {
                  handleFilterChange(item, e.target.value);
                }}
                fullWidth
                placeholder={FILTER_OPTIONS[index]}
                onKeyDown={handleKeyDown}
                InputProps={{
                  endAdornment: filters[item] && (
                    <ClearIcon
                      onClick={() => {
                        handleFilterChange(item, "");
                      }}
                      style={{ cursor: "pointer" }}
                    />
                  ),
                }}
              />
            </Grid>
          );
        })}
        <Grid item xs={2}>
          <SearchButton />
        </Grid>
        <Grid item xs={2}>
          <ResetFilterButton />
        </Grid>
      </React.Fragment>
    );
  };

  return (
    <ContentBody title={title}>
      <Container className={classes.container}>
        <Grid container>
          <Grid container item xs={12} direction={"row"} spacing={2} style={{ paddingBottom: "10px" }}>
            <Grid container justify={"space-between"} item xs={4} spacing={1}>
              <Grid item xs={3}>
                <Button
                  className={classes.button_color}
                  onClick={() => simpleDateHandler(3)}
                  variant="contained"
                  align="center"
                  fullWidth
                >
                  금년
                </Button>
              </Grid>
              <Grid item xs={3}>
                <Button
                  className={classes.button_color}
                  onClick={() => simpleDateHandler(0)}
                  variant="contained"
                  align="center"
                  fullWidth
                >
                  최근 1년
                </Button>
              </Grid>
              <Grid item xs={3}>
                <Button
                  className={classes.button_color}
                  onClick={() => simpleDateHandler(1)}
                  variant="contained"
                  align="center"
                  fullWidth
                >
                  최근 3개월
                </Button>
              </Grid>
              <Grid item xs={3}>
                <Button
                  className={classes.button_color}
                  onClick={() => simpleDateHandler(2)}
                  variant="contained"
                  align="center"
                  fullWidth
                >
                  최근 1개월
                </Button>
              </Grid>
              <DatePicker />
            </Grid>
            <Grid item xs={1}>
              <BottomNavigation
                showLabels
                value={onlyUpdated}
                onChange={onlyUpdatedHandler}
                style={{
                  border: "1px solid #464646",
                  borderRadius: "9px",
                  height: "80%",
                  width: "100%",
                }}
              >
                <BottomNavigationAction
                  label={
                    <Typography variant="body2" style={{ fontSize: "0.75rem" }}>
                      My PJT
                    </Typography>
                  }
                  value="my_project"
                  icon={<AccountBoxIcon size="small" />}
                  className={classes.navStyle}
                  style={
                    onlyUpdated === "my_project"
                      ? {
                          backgroundColor: "#464646",
                          color: "#FFFFFF",
                          minWidth: "10px",
                        }
                      : { color: "#D3D3D3", minWidth: "10px" }
                  }
                />
                <BottomNavigationAction
                  label={
                    <Typography variant="body2" style={{ fontSize: "0.75rem" }}>
                      All
                    </Typography>
                  }
                  value="all"
                  icon={<ListIcon size="small" />}
                  className={classes.navStyle}
                  style={
                    onlyUpdated === "all"
                      ? {
                          backgroundColor: "#464646",
                          color: "#FFFFFF",
                          minWidth: "10px",
                        }
                      : { color: "#D3D3D3", minWidth: "10px" }
                  }
                />
              </BottomNavigation>
            </Grid>
            <Grid container item xs={7} spacing={1}>
              <FiltersTextField />
            </Grid>
          </Grid>
          <Grid container item xs={12}>
            <StandbyProjectStatusTable
              filteredData={filteredData}
              userHistoryData={userHistoryData}
              currentUser={email.split("@")[0]}
              mutationHandlers={mutationHandlers}
            />
          </Grid>
        </Grid>
      </Container>
    </ContentBody>
  );
};

export default StandbyProjectStatus;
